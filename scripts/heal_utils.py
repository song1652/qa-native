"""
힐링 공용 유틸리티.

06_heal.py와 99_merge.py에서 공통으로 사용하는 함수들을 모아놓은 모듈.
- classify_error: traceback → 오류 유형 분류
- extract_key_lines: traceback에서 핵심 라인 추출
- append_lessons: lessons_learned.md 자동 기록
- find_screenshot_for_test: 스크린샷 검색
"""
import json
import re
from datetime import datetime
from pathlib import Path

from _paths import PROJECT_ROOT, read_state, write_state

LESSONS_PATH = PROJECT_ROOT / "agents" / "lessons_learned.md"
SCREENSHOTS_DIR = PROJECT_ROOT / "tests" / "screenshots"
HEAL_STATS_PATH = PROJECT_ROOT / "state" / "heal_stats.json"


def classify_error(traceback: str) -> str:
    """traceback에서 오류 유형 분류."""
    tb = traceback.lower()
    if any(k in tb for k in ["strict mode violation", "element not found",
                              "locator", "no element", "getby"]):
        return "Locator"
    if any(k in tb for k in ["expected", "to contain", "assertionerror",
                              "to have text", "to have url"]):
        return "Assertion"
    if "timeout" in tb:
        return "Timeout"
    if any(k in tb for k in ["url", "goto", "navigation"]):
        return "URL"
    return "기타"


def extract_key_lines(traceback: str) -> list[str]:
    """트레이스백에서 핵심 오류 라인 최대 3개 추출."""
    lines = traceback.splitlines()
    key = [line.strip() for line in lines
           if any(k in line for k in ["Error", "Expected", "assert",
                                       "expect", "Locator"])]
    return key[:3]


def find_screenshot_for_test(test_name: str) -> dict | None:
    """tests/screenshots/ 에서 테스트명에 매칭되는 스크린샷과 메타데이터를 찾는다."""
    if not SCREENSHOTS_DIR.exists():
        return None
    # 그룹 접두사 패턴 우선 검색 (group__test_name.png)
    candidates = list(SCREENSHOTS_DIR.glob(f"*__{test_name}.png"))
    if not candidates:
        # 이전 형식 fallback (test_name.png)
        candidates = list(SCREENSHOTS_DIR.glob(f"{test_name}.png"))
    if not candidates:
        return None
    shot_path = candidates[0]
    result = {"path": str(shot_path)}
    meta_path = shot_path.with_suffix("").with_suffix(".meta.json")
    if meta_path.exists():
        try:
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
            result["url"] = meta.get("url")
            result["timestamp"] = meta.get("timestamp")
        except Exception:
            pass
    return result


def append_lessons(failures: list[dict]) -> None:
    """실패 케이스를 lessons_learned.md에 자동 추가."""
    if not failures:
        return

    new_entries: dict[str, list[str]] = {}

    for f in failures:
        error_type = classify_error(f["traceback"])
        key_lines = extract_key_lines(f["traceback"])
        error_summary = key_lines[0] if key_lines else "(traceback 없음)"
        fix_hint = ""
        if error_type == "Locator":
            fix_hint = "dom_info 셀렉터 재확인, #id 우선 사용"
        elif error_type == "Assertion":
            fix_hint = "실제 페이지 텍스트/상태로 기댓값 수정"
        elif error_type == "Timeout":
            fix_hint = "expect(..., timeout=10000) 또는 wait_for_selector 추가"
        elif error_type == "URL":
            fix_hint = "BASE_URL 또는 goto 인자 재확인"

        entry = f"- **{error_type}**: `{error_summary}` — {fix_hint}\n"
        new_entries.setdefault(error_type, []).append(entry)

    if not LESSONS_PATH.exists():
        return

    content = LESSONS_PATH.read_text(encoding="utf-8")

    for section, entries in new_entries.items():
        section_header = f"## {section} 오류" if section != "기타" else "## 기타"
        insert_text = "\n" + "".join(entries)
        pattern = rf"({re.escape(section_header)}[^\n]*\n(?:<!--[^>]*-->\n)?)"
        if re.search(pattern, content):
            content = re.sub(pattern, r"\1" + insert_text, content, count=1)
        else:
            content += f"\n{section_header}\n{insert_text}"

    LESSONS_PATH.write_text(content, encoding="utf-8")
    print(f"[heal_utils] lessons_learned.md 업데이트: "
          f"{sum(len(v) for v in new_entries.values())}건 추가")


def update_heal_stats(failures: list[dict]) -> None:
    """heal_stats.json에 오류 패턴별 빈도를 업데이트한다."""
    if not failures:
        return
    try:
        if HEAL_STATS_PATH.exists():
            stats = read_state(HEAL_STATS_PATH)
        else:
            stats = {"version": 1, "patterns": {}}
        patterns = stats.setdefault("patterns", {})
        for f in failures:
            error_type = classify_error(f["traceback"])
            key_lines = extract_key_lines(f["traceback"])
            summary = key_lines[0].strip()[:120] if key_lines else "unknown"
            pattern_key = f"{error_type}::{summary}"
            if pattern_key in patterns:
                patterns[pattern_key]["count"] += 1
                patterns[pattern_key]["last_seen"] = datetime.now().isoformat()
            else:
                patterns[pattern_key] = {
                    "count": 1,
                    "error_type": error_type,
                    "summary": summary,
                    "first_seen": datetime.now().isoformat(),
                    "last_seen": datetime.now().isoformat(),
                }
        write_state(HEAL_STATS_PATH, stats)
        print(f"[heal_utils] heal_stats.json 업데이트: {len(failures)}건 기록")
    except Exception as e:
        print(f"[heal_utils] heal_stats.json 업데이트 실패 (무시): {e}")
