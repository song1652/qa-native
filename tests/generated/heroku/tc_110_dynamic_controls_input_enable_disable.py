"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/dynamic_controls
케이스: tc_110_dynamic_controls_input_enable_disable (tc_110)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com"


def test_tc_110_dynamic_controls_input_enable_disable(page):
    """Dynamic Controls 입력 필드 활성화 후 비활성화"""
    page.goto(f"{BASE_URL}/dynamic_controls")
    page.wait_for_load_state("networkidle")

    text_input = page.locator("#input-example input[type=text]")

    # Initially disabled
    expect(text_input).to_be_disabled()

    # Click Enable
    page.locator("#input-example button").click()

    # Wait for "It's enabled!" message
    expect(page.locator("#message")).to_contain_text("It's enabled!", timeout=10000)
    expect(text_input).to_be_enabled()

    # Type text to confirm it works
    text_input.fill("test input")

    # Click Disable
    page.locator("#input-example button").click()

    # Wait for "It's disabled!" message
    expect(page.locator("#message")).to_contain_text("It's disabled!", timeout=10000)
    expect(text_input).to_be_disabled()
