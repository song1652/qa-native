"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/dynamic_loading/1
케이스: tc_98_dynamic_loading_example_1 (tc_98)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com"


def test_tc_98_dynamic_loading_example_1(page):
    """Dynamic Loading Example 1 숨김에서 표시"""
    page.goto(f"{BASE_URL}/dynamic_loading/1")
    page.wait_for_load_state("networkidle")

    page.locator("#start button").click()

    finish = page.locator("#finish")
    expect(finish).to_be_visible(timeout=10000)
    expect(finish).to_contain_text("Hello World!")
