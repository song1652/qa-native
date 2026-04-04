"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: test_js_alert (tc_07)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"


def test_js_alert(page):
    """JS Alert 확인 — Alert 발생 및 OK 클릭 후 결과 텍스트 확인"""
    page.goto(BASE_URL + "javascript_alerts")

    page.on("dialog", lambda dialog: dialog.accept())

    page.locator("button", has_text="Click for JS Alert").click()

    expect(page.locator("#result")).to_contain_text(
        "You successfully clicked an alert", timeout=5000
    )
