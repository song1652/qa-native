"""훅 스크립트 공통 유틸리티."""
import sys
from pathlib import Path
from _paths import read_state


def check_state(path: Path, key: str, value: str, extra_check=None) -> dict | None:
    """상태 파일을 읽고 key=value 조건을 확인한다.

    Args:
        path: 상태 JSON 파일 경로
        key: 확인할 딕셔너리 키 (예: "step", "status")
        value: 기대하는 값
        extra_check: state dict를 받아 bool을 반환하는 선택적 함수.
                     False 반환 시 None을 돌려준다.

    Returns:
        조건을 모두 만족하면 state dict, 아니면 None.
        호출자는 None이면 sys.exit(0)을 수행해야 한다.
    """
    if not path.exists():
        return None

    try:
        state = read_state(path)
    except Exception:
        return None

    if state.get(key) != value:
        return None

    if extra_check is not None and not extra_check(state):
        return None

    return state
