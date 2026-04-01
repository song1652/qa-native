"""프로젝트 .venv가 있으면 해당 Python 경로를 반환하는 공통 헬퍼."""
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
_VENV_PYTHON = PROJECT_ROOT / ".venv" / "bin" / "python"
PYTHON_EXE = str(_VENV_PYTHON) if _VENV_PYTHON.exists() else sys.executable
