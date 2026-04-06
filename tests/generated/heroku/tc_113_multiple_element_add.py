"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_92_multiple_element_add (tc_113)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from pathlib import Path

BASE_URL = "https://the-internet.herokuapp.com/"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_tc_92_multiple_element_add(page):
    """Add multiple elements and verify count"""
    # TODO: Claude Code가 아래를 완성
    # 케이스 타입: structured
    # data_key: null
    # 전략: goto() → click(button[onclick='addElement()']) → click(button[onclick='addElement()']) → click(button[onclick='addElement()']) → click(button[onclick='addElement()']) → click(button[onclick='addElement()'])
    # 검증: visible: 5 Delete buttons present
    pass
