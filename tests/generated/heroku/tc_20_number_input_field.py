"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_20_number_input_field (tc_20)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_tc_20_number_input_field(page):
    """숫자 입력 필드"""
    page.goto(BASE_URL + "inputs")
    expect(page.locator("body")).to_be_visible()

    number_input = page.locator("input[type='number']")
    expect(number_input).to_be_visible()

    number_input.fill("42")

    expect(number_input).to_have_value("42")

    input_type = number_input.get_attribute("type")
    assert input_type == "number", f"Expected type='number', got: {input_type}"
