"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_29_context_menu_alert (tc_29)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
BASE_URL = "https://the-internet.herokuapp.com/"


def test_tc_29_context_menu_alert(page):
    """핫스팟 영역 우클릭 시 Alert 다이얼로그 표시 확인"""
    page.goto("https://the-internet.herokuapp.com/context_menu")
    alert_message = []

    def handle_dialog(dialog):
        alert_message.append(dialog.message)
        dialog.accept()

    page.on("dialog", handle_dialog)
    page.locator("#hot-spot").click(button="right")
    page.wait_for_timeout(1000)
    assert len(alert_message) > 0, "Expected an alert dialog to appear"
    assert "context menu" in alert_message[0].lower(), (
        f"Expected 'context menu' in alert message, got: {alert_message[0]}"
    )
