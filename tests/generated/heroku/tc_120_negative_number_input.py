"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_120_negative_number_input (tc_120)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_tc_120_negative_number_input(page):
    """숫자 입력 필드에 -100 입력 후 값 확인"""
    page.goto(BASE_URL + "inputs")
    page.wait_for_load_state("domcontentloaded")
    input_field = page.locator("input[type='number']")
    expect(input_field).to_be_visible(timeout=5000)
    input_field.fill("-100")
    expect(input_field).to_have_value("-100", timeout=5000)
