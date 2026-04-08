"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_61_notification_message (tc_61)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_tc_61_notification_message(page):
    """Click here 링크 클릭 후 플래시 알림 메시지에 Action 텍스트 포함 확인"""
    page.goto("https://the-internet.herokuapp.com/notification_message_rendered")
    page.wait_for_load_state("domcontentloaded")

    page.locator("a[href='/notification_message']").click()
    page.wait_for_load_state("domcontentloaded")

    flash = page.locator("#flash")
    expect(flash).to_be_visible(timeout=10000)
    expect(flash).to_contain_text("Action", timeout=5000)
