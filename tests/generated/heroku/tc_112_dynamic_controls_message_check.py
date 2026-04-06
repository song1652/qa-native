"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/dynamic_controls
케이스: tc_112_dynamic_controls_message_check (tc_112)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com"


def test_tc_112_dynamic_controls_message_check(page):
    """Dynamic Controls 메시지 확인"""
    page.goto(f"{BASE_URL}/dynamic_controls")
    page.wait_for_load_state("networkidle")

    # Click Remove button in checkbox-example
    page.locator("#checkbox-example button").click()

    # Wait for #message to show "It's gone!"
    message = page.locator("#message")
    expect(message).to_contain_text("It's gone!", timeout=10000)
    expect(message).to_be_visible()
