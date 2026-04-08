"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_20_number_input (tc_20)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from pathlib import Path

BASE_URL = "https://the-internet.herokuapp.com/"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_tc_20_number_input(page):
    """숫자 입력 필드에 42 입력 후 value 및 type=number 확인"""
    # TODO: Claude Code가 아래를 완성
    # 케이스 타입: structured
    # data_key: null
    # 전략: goto() → fill(input[type='number'])
    # 검증: element_visible: input value=42, type=number
    pass
