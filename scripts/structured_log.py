"""구조화된 로그 (JSON Lines) — 각 스크립트에서 import하여 사용.

기존 print 출력은 유지하면서, 병행하여 JSON Lines 파일에 구조화된 이벤트를 기록한다.
로그 파일: logs/structured.jsonl

사용법:
    from structured_log import slog
    slog("step_start", step="01_analyze", url="https://example.com")
    slog("step_end", step="01_analyze", duration_sec=3.2)
    slog("test_fail", test_name="test_login", error_type="Locator", summary="...")
    slog("heal_skip", test_name="test_login", reason="동일 오류 2회 반복")
"""
import json
from datetime import datetime
from pathlib import Path

try:
    import fcntl
except ImportError:
    fcntl = None  # Windows 환경

_LOG_DIR = Path(__file__).resolve().parent.parent / "logs"
_LOG_FILE = _LOG_DIR / "structured.jsonl"


def slog(event: str, **kwargs) -> None:
    """구조화된 이벤트를 JSON Lines로 기록한다.

    Args:
        event: 이벤트 타입 (예: step_start, step_end, test_fail, heal_patch 등)
        **kwargs: 이벤트별 추가 데이터
    """
    _LOG_DIR.mkdir(parents=True, exist_ok=True)
    entry = {
        "ts": datetime.now().isoformat(),
        "event": event,
        **kwargs,
    }
    line = json.dumps(entry, ensure_ascii=False) + "\n"
    try:
        with open(_LOG_FILE, "a", encoding="utf-8") as f:
            if fcntl:
                fcntl.flock(f, fcntl.LOCK_EX)
            try:
                f.write(line)
            finally:
                if fcntl:
                    fcntl.flock(f, fcntl.LOCK_UN)
    except Exception:
        pass  # 로그 실패가 파이프라인을 중단하면 안 됨
