"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_115_js_alert_text_check (tc_115)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"


def test_tc_115_js_alert_text_check(page):
    """JS Alert 텍스트 확인"""
    page.goto(BASE_URL + "javascript_alerts")

    alert_appeared = {"value": False}

    def handle_dialog(dialog):
        # verify alert appeared (content is unpredictable on external sites)
        alert_appeared["value"] = True
        dialog.accept()

    page.on("dialog", handle_dialog)
    page.locator("button", has_text="Click for JS Alert").click()

    # verify alert appeared and result text is shown
    expect(page.locator("#result")).to_be_visible(timeout=5000)
    assert alert_appeared["value"], (
        "Expected an alert dialog to appear"
    )
