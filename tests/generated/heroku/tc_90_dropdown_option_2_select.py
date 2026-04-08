"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_90_dropdown_option_2_select (tc_90)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"


def test_tc_90_dropdown_option_2_select(page):
    """드롭다운에서 Option 2 선택 후 value=2 확인"""
    page.goto("https://the-internet.herokuapp.com/dropdown")
    page.wait_for_load_state("domcontentloaded")

    dropdown = page.locator("#dropdown")
    dropdown.select_option("2")

    expect(dropdown).to_have_value("2")
