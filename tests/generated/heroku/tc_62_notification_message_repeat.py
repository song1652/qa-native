"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_62_notification_message_repeat (tc_62)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_tc_62_notification_message_repeat(page):
    """반복 클릭 시 알림 메시지가 새로 표시되는지 확인"""
    page.goto("https://the-internet.herokuapp.com/notification_message_rendered")
    page.wait_for_load_state("domcontentloaded")

    # First click
    page.locator("a[href='/notification_message']").click()
    page.wait_for_load_state("domcontentloaded")
    flash = page.locator("#flash")
    expect(flash).to_be_visible(timeout=10000)
    first_text = flash.inner_text()

    # Second click
    page.locator("a[href='/notification_message']").click()
    page.wait_for_load_state("domcontentloaded")
    flash2 = page.locator("#flash")
    expect(flash2).to_be_visible(timeout=10000)
    second_text = flash2.inner_text()

    assert "Action" in first_text or "Action" in second_text
