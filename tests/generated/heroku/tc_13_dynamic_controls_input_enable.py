"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/dynamic_controls
케이스: test_dynamic_controls_input_enable (tc_13)
"""
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com"


def test_dynamic_controls_input_enable(page):
    """Dynamic Controls 입력 필드 활성화"""
    page.goto(f"{BASE_URL}/dynamic_controls")

    text_input = page.locator("#input-example input[type=text]")
    button = page.locator("#input-example button")

    # 초기 상태: disabled
    expect(text_input).to_be_disabled()

    # Enable 클릭
    button.click()
    expect(page.locator("#message")).to_contain_text("It's enabled!", timeout=10000)
    expect(text_input).to_be_enabled(timeout=10000)
