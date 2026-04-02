"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/javascript_alerts
케이스: test_js_alert (tc_07)
"""
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com"


def test_js_alert(page):
    """JS Alert 확인 — Alert OK 후 결과 텍스트 검증"""
    page.goto(f"{BASE_URL}/javascript_alerts")

    page.on("dialog", lambda dialog: dialog.accept())
    page.locator("button", has_text="Click for JS Alert").click()

    expect(page.locator("#result")).to_contain_text(
        "You successfully clicked an alert"
    )
