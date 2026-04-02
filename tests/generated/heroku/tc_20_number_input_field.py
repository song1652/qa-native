"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/inputs
케이스: test_number_input_field (tc_20)
"""
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com"


def test_number_input_field(page):
    """숫자 입력 필드 — 42 입력 후 값 확인"""
    page.goto(f"{BASE_URL}/inputs")

    number_input = page.locator("input[type=number]")
    number_input.fill("42")

    expect(number_input).to_have_value("42")
    assert number_input.get_attribute("type") == "number"
