"""프로젝트 .venv가 있으면 해당 Python 경로를 반환하는 공통 헬퍼."""
import sys
from _paths import PROJECT_ROOT

# Windows: Scripts/python.exe, Unix: bin/python
_VENV_WIN = PROJECT_ROOT / ".venv" / "Scripts" / "python.exe"
_VENV_UNIX = PROJECT_ROOT / ".venv" / "bin" / "python"
_VENV_PYTHON = _VENV_WIN if _VENV_WIN.exists() else _VENV_UNIX
PYTHON_EXE = str(_VENV_PYTHON) if _VENV_PYTHON.exists() else sys.executable
