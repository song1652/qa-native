"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_114_js_prompt_empty_value (tc_114)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"


def test_tc_114_js_prompt_empty_value(page):
    """JS Prompt 빈값 확인"""
    page.goto(BASE_URL + "javascript_alerts")

    # accept the prompt with empty string (no input)
    page.on("dialog", lambda dialog: dialog.accept(""))
    page.locator("button", has_text="Click for JS Prompt").click()

    expect(page.locator("#result")).to_contain_text(
        "You entered:", timeout=5000
    )
