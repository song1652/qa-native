"""프로젝트 상태/로그 파일 경로 상수 + 안전한 JSON 읽기/쓰기."""
import fcntl
import hashlib
import json
import os
import tempfile
from datetime import datetime, timedelta
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# 상태 파일
STATE_DIR = PROJECT_ROOT / "state"
PIPELINE_STATE = STATE_DIR / "pipeline.json"
DISCUSS_STATE = STATE_DIR / "discuss.json"
PARALLEL_STATE = STATE_DIR / "parallel.json"
QUICK_STATE = STATE_DIR / "quick.json"
HEAL_CONTEXT_STATE = STATE_DIR / "heal_context.json"
RUN_HISTORY = STATE_DIR / "run_history.json"

# DOM 캐시
DOM_CACHE_DIR = STATE_DIR / "dom_cache"
DOM_CACHE_TTL_HOURS = int(os.environ.get("DOM_CACHE_TTL_HOURS", "168"))  # 7일

# 로그 파일
LOGS_DIR = PROJECT_ROOT / "logs"
RUN_QA_LOG = LOGS_DIR / "run_qa.txt"
RUN_PARALLEL_LOG = LOGS_DIR / "run_parallel.txt"
MERGE_LOG = LOGS_DIR / "merge.txt"
QUICK_RUN_LOG = LOGS_DIR / "quick_run.txt"


def append_run_history(entry: dict):
    """실행 이력을 state/run_history.json에 append한다."""
    RUN_HISTORY.parent.mkdir(parents=True, exist_ok=True)
    history = []
    if RUN_HISTORY.exists():
        try:
            with open(RUN_HISTORY, "r", encoding="utf-8") as f:
                fcntl.flock(f, fcntl.LOCK_SH)
                try:
                    history = json.loads(f.read())
                finally:
                    fcntl.flock(f, fcntl.LOCK_UN)
        except (json.JSONDecodeError, Exception):
            history = []
    history.append(entry)
    content = json.dumps(history, ensure_ascii=False, indent=2)
    fd, tmp_path = tempfile.mkstemp(dir=RUN_HISTORY.parent, suffix=".tmp")
    try:
        with open(fd, "w", encoding="utf-8") as f:
            f.write(content)
        Path(tmp_path).replace(RUN_HISTORY)
    except Exception:
        Path(tmp_path).unlink(missing_ok=True)
        raise


def get_cached_dom(url: str) -> dict | None:
    """캐시된 DOM 분석 결과가 있으면 반환. TTL 초과 시 None."""
    cache_file = DOM_CACHE_DIR / f"{hashlib.md5(url.encode()).hexdigest()}.json"
    if cache_file.exists():
        try:
            data = json.loads(cache_file.read_text(encoding="utf-8"))
            cached_at = data.get("_cached_at")
            if cached_at and DOM_CACHE_TTL_HOURS > 0:
                try:
                    ts = datetime.fromisoformat(cached_at)
                    if datetime.now() - ts > timedelta(hours=DOM_CACHE_TTL_HOURS):
                        return None  # expired
                except (ValueError, TypeError):
                    pass
            return data
        except Exception:
            pass
    return None


def save_dom_cache(url: str, dom: dict):
    """DOM 분석 결과를 캐시에 저장 (timestamp 포함). 원본 dict를 변경하지 않음."""
    DOM_CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cache_data = {**dom, "_cached_at": datetime.now().isoformat()}
    cache_file = DOM_CACHE_DIR / f"{hashlib.md5(url.encode()).hexdigest()}.json"
    content = json.dumps(cache_data, ensure_ascii=False, indent=2)
    fd, tmp_path = tempfile.mkstemp(dir=DOM_CACHE_DIR, suffix=".tmp")
    try:
        with open(fd, "w", encoding="utf-8") as f:
            f.write(content)
        Path(tmp_path).replace(cache_file)
    except Exception:
        Path(tmp_path).unlink(missing_ok=True)
        raise


def resolve_sub_doms(state: dict) -> dict:
    """sub_dom_keys에서 캐시 파일을 로드하여 {url: dom} 매핑 반환."""
    sub_dom_keys = state.get("sub_dom_keys", {})
    result = {}
    for url in sub_dom_keys:
        dom = get_cached_dom(url)
        if dom:
            result[url] = dom
    return result


def read_state(path: Path) -> dict:
    """파일 잠금으로 안전하게 JSON 상태 파일을 읽는다."""
    if not path.exists():
        return {}
    with open(path, "r", encoding="utf-8") as f:
        fcntl.flock(f, fcntl.LOCK_SH)
        try:
            return json.loads(f.read())
        finally:
            fcntl.flock(f, fcntl.LOCK_UN)


def write_state(path: Path, data: dict):
    """원자적 쓰기로 안전하게 JSON 상태 파일을 쓴다."""
    path.parent.mkdir(parents=True, exist_ok=True)
    content = json.dumps(data, ensure_ascii=False, indent=2)
    fd, tmp_path = tempfile.mkstemp(dir=path.parent, suffix=".tmp")
    try:
        with open(fd, "w", encoding="utf-8") as f:
            f.write(content)
        Path(tmp_path).replace(path)
    except Exception:
        Path(tmp_path).unlink(missing_ok=True)
        raise
