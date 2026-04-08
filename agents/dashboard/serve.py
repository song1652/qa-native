"""
QA Agent Dashboard 서버
프로젝트 루트 또는 어디서든 실행 가능:
  python agents/dashboard/serve.py
"""
import json
import queue
import re
import sys
import threading
import time
import webbrowser
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from pathlib import Path

PORT = 8765
HERE = Path(__file__).parent                    # agents/dashboard/
PROJECT_ROOT = HERE.parent.parent               # qa-native/
DIALOG_PATH = PROJECT_ROOT / "agents" / "dialog.json"
STATE_PATH = PROJECT_ROOT / "state.json"
TEAM_NOTES_PATH = PROJECT_ROOT / "agents" / "team_notes.md"
DISCUSS_PATH = PROJECT_ROOT / "discuss_state.json"
PENDING_IMPL_PATH = PROJECT_ROOT / "pending_impl.json"

# ── SSE 클라이언트 관리 ────────────────────────────────────────
_sse_clients: list[queue.Queue] = []
_sse_lock = threading.Lock()


def _sse_notify():
    """dialog.json 변경 시 모든 SSE 클라이언트에 알림."""
    with _sse_lock:
        dead = []
        for q in _sse_clients:
            try:
                q.put_nowait("update")
            except queue.Full:
                dead.append(q)
        for q in dead:
            _sse_clients.remove(q)


def _watch_files():
    """dialog.json / discuss_state.json mtime을 0.3초마다 감시."""
    watched = [DIALOG_PATH, DISCUSS_PATH]
    last_mtimes = {p: 0.0 for p in watched}
    while True:
        for p in watched:
            try:
                mtime = p.stat().st_mtime if p.exists() else 0.0
                if mtime != last_mtimes[p]:
                    last_mtimes[p] = mtime
                    _sse_notify()
            except Exception:
                pass
        time.sleep(0.3)


# 파일 감시 스레드 시작
threading.Thread(target=_watch_files, daemon=True).start()

TEAM_NOTES_HEADER = (
    "# 팀 결정 사항\n\n"
    "> **독자**: 심의 Agent — 팀 토론 결론 누적. 토론 시 중복 결론 방지 목적으로 참조.\n\n"
    "---\n"
)


def load_json(path: Path):
    if path.exists():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            return None
    return None


def parse_conclusion_items(conclusion: str) -> list:
    """결론 마크다운을 투표 가능한 개별 항목으로 파싱."""
    items = []

    # 1) ### 소제목 파싱
    for m in re.finditer(r'^###\s+(.+?)\n([\s\S]*?)(?=^###\s|\Z)', conclusion, re.MULTILINE):
        title = m.group(1).strip()
        body  = re.sub(r'\n?---+\s*$', '', m.group(2)).strip()
        items.append({"id": len(items), "title": title, "text": body, "status": "pending"})

    # 2) 번호 목록 파싱 (1. **title**: body)
    for m in re.finditer(r'^\d+\.\s+(.+)$', conclusion, re.MULTILINE):
        text = m.group(1).strip()
        bold = re.match(r'\*\*(.+?)\*\*[:\s]*(.*)', text)
        title = bold.group(1).strip() if bold else text[:70]
        items.append({"id": len(items), "title": title, "text": text, "status": "pending"})

    # 3) fallback
    if not items:
        items.append({"id": 0, "title": "전체 결론", "text": conclusion, "status": "pending"})

    return items


def finalize_team_notes(discuss: dict):
    """승인된 항목만 team_notes.md에 덮어쓰기 + pending_impl.json 생성."""
    import datetime
    items = discuss.get("conclusion_items", [])
    approved = [i for i in items if i["status"] == "approved"]
    topic = discuss.get("topic", "")
    today = datetime.datetime.now().strftime("%Y-%m-%d")

    content = TEAM_NOTES_HEADER
    if approved:
        content += f"\n## {topic}\n> 결정일: {today}\n\n"
        for item in approved:
            content += f"### {item['title']}\n{item['text']}\n\n"
        content += "---\n"

    TEAM_NOTES_PATH.write_text(content, encoding="utf-8")

    # 구현 대기 파일 생성 → UserPromptSubmit 훅이 감지해 Claude에 주입
    if approved:
        pending = {
            "status": "pending",
            "topic": topic,
            "approved_at": datetime.datetime.now().isoformat(),
            "items": approved,
        }
        PENDING_IMPL_PATH.write_text(
            json.dumps(pending, ensure_ascii=False, indent=2), encoding="utf-8"
        )


def build_dialogs() -> dict:
    """팀 토론 대화 payload 반환 (dialog.json은 팀 토론 전용)."""
    full_dialog = load_json(DIALOG_PATH) or {"sessions": []}
    discuss_state = load_json(DISCUSS_PATH) or {}

    # step=discussed 이고 conclusion_items 없으면 자동 파싱
    if (discuss_state.get("step") == "discussed"
            and discuss_state.get("conclusion")
            and not discuss_state.get("conclusion_items")):
        discuss_state["conclusion_items"] = parse_conclusion_items(discuss_state["conclusion"])
        DISCUSS_PATH.write_text(
            json.dumps(discuss_state, ensure_ascii=False, indent=2), encoding="utf-8"
        )

    all_sessions = full_dialog.get("sessions", [])
    team_sessions = [s for s in all_sessions if s.get("stage") == "team_discussion"]

    return {
        "team_sessions": team_sessions,
        "discuss_state": discuss_state,
    }


class DashboardHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path.split("?")[0]
        if path in ("/", "/index.html"):
            self._serve_file(HERE / "index.html", "text/html; charset=utf-8")
        elif path == "/api/dialogs":
            payload = build_dialogs()
            self._serve_bytes(
                json.dumps(payload, ensure_ascii=False).encode("utf-8"),
                "application/json; charset=utf-8"
            )
        elif path == "/api/events":
            self._serve_sse()
        elif path == "/api/dialog":
            self._serve_json(DIALOG_PATH)
        elif path == "/api/state":
            self._serve_json(STATE_PATH)
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        path = self.path.split("?")[0]
        try:
            self._handle_post(path)
        except Exception as e:
            import traceback
            traceback.print_exc()
            msg = json.dumps({"ok": False, "error": str(e)}, ensure_ascii=False).encode("utf-8")
            try:
                self._serve_bytes(msg, "application/json; charset=utf-8")
            except Exception:
                pass

    def _handle_post(self, path):
        # ── 대화 초기화 ──────────────────────────────────────────
        if path == "/api/reset":
            empty = {"pipeline_url": "", "started_at": "", "sessions": []}
            DIALOG_PATH.write_text(
                json.dumps(empty, ensure_ascii=False, indent=2), encoding="utf-8"
            )
            self._serve_bytes(b'{"ok":true}', "application/json; charset=utf-8")

        # ── 토론 시작 ─────────────────────────────────────────────
        elif path == "/api/discuss/start":
            import datetime
            length = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(length).decode("utf-8"))
            topic = body.get("topic", "").strip()
            if not topic:
                self._serve_bytes(b'{"ok":false,"error":"topic required"}',
                                  "application/json; charset=utf-8")
                return

            history = []
            if DISCUSS_PATH.exists():
                try:
                    prev = json.loads(DISCUSS_PATH.read_text(encoding="utf-8"))
                    history = prev.get("history", [])
                    if prev.get("step") in ("approved", "rejected", "discussed"):
                        history.append({k: v for k, v in prev.items() if k != "history"})
                except Exception:
                    pass

            discuss = {
                "topic": topic, "step": "pending", "conclusion": "",
                "rejection_reason": "", "rejection_count": 0,
                "created_at": datetime.datetime.now().isoformat(),
                "history": history,
            }
            DISCUSS_PATH.write_text(
                json.dumps(discuss, ensure_ascii=False, indent=2), encoding="utf-8"
            )

            # Claude Code UserPromptSubmit 훅(check_pending_discuss.py)이
            # 다음 프롬프트 제출 시 자동으로 토론 시작을 Claude에게 주입한다.
            self._serve_bytes(b'{"ok":true}',
                              "application/json; charset=utf-8")

        # ── 항목별 투표 ───────────────────────────────────────────
        elif path == "/api/discuss/vote_item":
            length = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(length).decode("utf-8"))
            item_id = int(body.get("item_id", -1))
            vote    = body.get("vote", "")  # "approve" | "reject"

            if not DISCUSS_PATH.exists():
                self._serve_bytes(
                    json.dumps({"ok": False, "error": "discuss_state.json 없음"}, ensure_ascii=False).encode("utf-8"),
                    "application/json; charset=utf-8")
                return

            discuss = json.loads(DISCUSS_PATH.read_text(encoding="utf-8"))
            items = discuss.get("conclusion_items", [])
            for item in items:
                if item["id"] == item_id:
                    item["status"] = "approved" if vote == "approve" else "rejected"
                    break
            discuss["conclusion_items"] = items

            all_voted = bool(items) and all(i["status"] != "pending" for i in items)
            if all_voted:
                finalize_team_notes(discuss)
                discuss["step"] = "approved"

            DISCUSS_PATH.write_text(
                json.dumps(discuss, ensure_ascii=False, indent=2), encoding="utf-8"
            )
            self._serve_bytes(
                json.dumps({"ok": True, "all_voted": all_voted}, ensure_ascii=False).encode("utf-8"),
                "application/json; charset=utf-8"
            )

        # ── 전체 반려 ─────────────────────────────────────────────
        elif path == "/api/discuss/reject":
            length = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(length).decode("utf-8")) if length else {}
            reason = body.get("reason", "").strip()
            if not DISCUSS_PATH.exists():
                self._serve_bytes(
                    json.dumps({"ok": False, "error": "discuss_state.json 없음"}, ensure_ascii=False).encode("utf-8"),
                    "application/json; charset=utf-8")
                return
            discuss = json.loads(DISCUSS_PATH.read_text(encoding="utf-8"))
            discuss["step"] = "rejected"
            discuss["rejection_reason"] = reason
            discuss["rejection_count"] = discuss.get("rejection_count", 0) + 1
            DISCUSS_PATH.write_text(
                json.dumps(discuss, ensure_ascii=False, indent=2), encoding="utf-8"
            )
            self._serve_bytes(b'{"ok":true}', "application/json; charset=utf-8")

        else:
            self.send_response(404)
            self.end_headers()

    def _serve_sse(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream; charset=utf-8")
        self.send_header("Cache-Control", "no-cache")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("X-Accel-Buffering", "no")
        self.end_headers()

        q: queue.Queue = queue.Queue(maxsize=10)
        with _sse_lock:
            _sse_clients.append(q)

        def send(data: str):
            self.wfile.write(f"data: {data}\n\n".encode("utf-8"))
            self.wfile.flush()

        try:
            # 연결 즉시 현재 상태 전송
            send(json.dumps(build_dialogs(), ensure_ascii=False))
            while True:
                try:
                    q.get(timeout=15)
                    send(json.dumps(build_dialogs(), ensure_ascii=False))
                except queue.Empty:
                    # keepalive
                    self.wfile.write(b": ping\n\n")
                    self.wfile.flush()
        except Exception:
            pass
        finally:
            with _sse_lock:
                if q in _sse_clients:
                    _sse_clients.remove(q)

    def _serve_file(self, path: Path, content_type: str):
        if path.exists():
            content = path.read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)
        else:
            self.send_response(404)
            self.end_headers()

    def _serve_json(self, path: Path):
        content = path.read_bytes() if path.exists() else b'{"pipeline_url":"","started_at":"","sessions":[]}'
        self._serve_bytes(content, "application/json; charset=utf-8")

    def _serve_bytes(self, content: bytes, content_type: str):
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cache-Control", "no-cache")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def log_message(self, format, *args):
        print(f"[{self.log_date_time_string()}] {format % args}")


def main():
    server = ThreadingHTTPServer(("localhost", PORT), DashboardHandler)
    url = f"http://localhost:{PORT}"
    print(f"[Dashboard] 서버 시작: {url}")
    print(f"[Dashboard] 종료: Ctrl+C")
    webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[Dashboard] 서버 종료")


if __name__ == "__main__":
    main()
