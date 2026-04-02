"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/dynamic_controls
케이스: test_dynamic_controls_checkbox_remove_add (tc_12)
"""
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com"


def test_dynamic_controls_checkbox_remove_add(page):
    """Dynamic Controls 체크박스 제거/추가"""
    page.goto(f"{BASE_URL}/dynamic_controls")

    checkbox = page.locator("#checkbox")
    button = page.locator("#checkbox-example button")

    # Remove 클릭
    button.click()
    expect(page.locator("#message")).to_contain_text("It's gone!", timeout=10000)
    expect(checkbox).to_be_hidden()

    # Add 클릭
    button.click()
    expect(page.locator("#message")).to_contain_text("It's back!", timeout=10000)
    expect(page.locator("#checkbox")).to_be_visible(timeout=10000)
