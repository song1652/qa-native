"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_29_context_menu_alert (tc_29)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_tc_29_context_menu_alert(page):
    """우클릭 컨텍스트 메뉴 Alert 발생"""
    page.goto(BASE_URL + "context_menu")
    expect(page.locator("#hot-spot")).to_be_visible()

    alert_fired = []

    def handle_dialog(dialog):
        alert_fired.append(dialog.message)
        dialog.accept()

    page.on("dialog", handle_dialog)
    page.locator("#hot-spot").click(button="right")
    page.wait_for_timeout(1000)

    assert len(alert_fired) > 0, "Expected alert to fire after right-click"
