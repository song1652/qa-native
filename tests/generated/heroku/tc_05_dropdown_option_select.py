"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/dropdown
케이스: test_dropdown_option_select (tc_05)
"""
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com"


def test_dropdown_option_select(page):
    """드롭다운 옵션 선택 — Option 1, Option 2 순서대로 선택"""
    page.goto(f"{BASE_URL}/dropdown")

    dropdown = page.locator("#dropdown")

    dropdown.select_option("1")
    expect(dropdown).to_have_value("1")

    dropdown.select_option("2")
    expect(dropdown).to_have_value("2")
