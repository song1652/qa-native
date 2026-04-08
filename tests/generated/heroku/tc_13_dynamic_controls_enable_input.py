"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_13_dynamic_controls_enable_input (tc_13)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from pathlib import Path

BASE_URL = "https://the-internet.herokuapp.com/"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_tc_13_dynamic_controls_enable_input(page):
    """입력 필드 비활성화 상태 확인 후 Enable 클릭하여 활성화 확인"""
    # TODO: Claude Code가 아래를 완성
    # 케이스 타입: structured
    # data_key: null
    # 전략: goto() → click(#input-example button) → wait(#message)
    # 검증: element_visible: #input-example input enabled
    pass
