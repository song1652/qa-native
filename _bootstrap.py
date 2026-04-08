"""프로젝트 진입점 공통 경로 설정.

루트 레벨 스크립트(run_qa.py, run_team.py 등)가 import하면
scripts/ 디렉토리가 sys.path에 추가된다.
"""
import sys
from pathlib import Path

_SCRIPTS_DIR = str(Path(__file__).resolve().parent / "scripts")
if _SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, _SCRIPTS_DIR)
