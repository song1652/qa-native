"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_06_js_confirm_accept (tc_06)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from pathlib import Path

BASE_URL = "https://the-internet.herokuapp.com/"
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_tc_06_js_confirm_accept(page):
    """JS Confirm 버튼 클릭 → dialog accept → #result에 You clicked: Ok 메시지 표시"""
    page.goto("https://the-internet.herokuapp.com/javascript_alerts")

    dialog_messages = []

    def handle_dialog(dialog):
        dialog_messages.append(dialog.message)
        dialog.accept()

    page.on("dialog", handle_dialog)
    page.locator("button", has_text="Click for JS Confirm").click()
    page.wait_for_timeout(500)

    assert any("JS Confirm" in m for m in dialog_messages), f"Expected JS Confirm dialog, got: {dialog_messages}"
    result = page.locator("#result")
    result.wait_for(state="visible", timeout=5000)
    assert "You clicked: Ok" in result.inner_text()
