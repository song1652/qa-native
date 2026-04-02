"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/dynamic_loading/1
케이스: test_dynamic_loading_element_wait (tc_18)
"""
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com"


def test_dynamic_loading_element_wait(page):
    """Dynamic Loading 요소 대기 — Start 후 Hello World! 표시"""
    page.goto(f"{BASE_URL}/dynamic_loading/1")

    page.locator("#start button").click()

    finish = page.locator("#finish")
    expect(finish).to_be_visible(timeout=15000)
    expect(finish).to_contain_text("Hello World!")
