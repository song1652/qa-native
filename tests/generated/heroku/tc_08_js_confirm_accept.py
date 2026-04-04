"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: test_js_confirm_accept (tc_08)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"


def test_js_confirm_accept(page):
    """JS Confirm 수락 — Confirm OK 후 결과 텍스트 확인"""
    page.goto(BASE_URL + "javascript_alerts")

    page.on("dialog", lambda dialog: dialog.accept())

    page.locator("button", has_text="Click for JS Confirm").click()

    expect(page.locator("#result")).to_contain_text(
        "You clicked: Ok", timeout=5000
    )
