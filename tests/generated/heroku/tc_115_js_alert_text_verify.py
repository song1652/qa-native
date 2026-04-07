"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_115_js_alert_text_verify (tc_115)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_tc_115_js_alert_text_verify(page):
    """JS Alert 다이얼로그 메시지 I am a JS Alert 확인 후 OK 클릭"""
    alert_message = []
    page.goto(BASE_URL + "javascript_alerts")
    page.wait_for_load_state("domcontentloaded")

    def handle_dialog(dialog):
        alert_message.append(dialog.message)
        dialog.accept()

    page.on("dialog", handle_dialog)
    page.locator("button[onclick='jsAlert()']").click()
    expect(page.locator("#result")).to_contain_text("You successfully clicked an alert", timeout=10000)
    assert "I am a JS Alert" in alert_message[0]
