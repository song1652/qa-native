"""프로젝트 상태/로그 파일 경로 상수 + 안전한 JSON 읽기/쓰기."""
import fcntl
import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# 상태 파일
STATE_DIR = PROJECT_ROOT / "state"
PIPELINE_STATE = STATE_DIR / "pipeline.json"
DISCUSS_STATE = STATE_DIR / "discuss.json"
PARALLEL_STATE = STATE_DIR / "parallel.json"
QUICK_STATE = STATE_DIR / "quick.json"
HEAL_CONTEXT_STATE = STATE_DIR / "heal_context.json"

# DOM 캐시
DOM_CACHE_DIR = STATE_DIR / "dom_cache"

# 로그 파일
LOGS_DIR = PROJECT_ROOT / "logs"
RUN_QA_LOG = LOGS_DIR / "run_qa.txt"
RUN_PARALLEL_LOG = LOGS_DIR / "run_parallel.txt"
MERGE_LOG = LOGS_DIR / "merge.txt"
QUICK_RUN_LOG = LOGS_DIR / "quick_run.txt"


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
    """원자적 쓰기로 안전하게 JSON 상태 파일을 쓴다.

    임시 파일에 쓴 뒤 rename하므로 읽기 중인 프로세스가
    불완전한 파일을 보지 않는다.
    """
    import tempfile
    path.parent.mkdir(parents=True, exist_ok=True)
    content = json.dumps(data, ensure_ascii=False, indent=2)
    fd, tmp_path = tempfile.mkstemp(dir=path.parent, suffix=".tmp")
    try:
        with open(fd, "w", encoding="utf-8") as f:
            f.write(content)
        Path(tmp_path).replace(path)  # atomic rename on POSIX
    except Exception:
        Path(tmp_path).unlink(missing_ok=True)
        raise
