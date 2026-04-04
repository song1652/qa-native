"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: test_dropdown_select_option (tc_05)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"


def test_dropdown_select_option(page):
    """드롭다운 옵션 선택 — Option 1, Option 2 순서 선택 후 value 확인"""
    page.goto(BASE_URL + "dropdown")

    dropdown = page.locator("#dropdown")

    dropdown.select_option("1")
    expect(dropdown).to_have_value("1", timeout=5000)

    dropdown.select_option("2")
    expect(dropdown).to_have_value("2", timeout=5000)
