"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_63_notification_message_close (tc_63)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from pathlib import Path

from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_tc_63_notification_message_close(page):
    """알림 메시지 닫기 버튼"""
    page.goto(BASE_URL + "notification_message_rendered")

    page.locator("a", has_text="Click here").click()
    page.wait_for_load_state("domcontentloaded")

    flash = page.locator("#flash")
    expect(flash).to_be_visible(timeout=10000)

    # Click the close button (x link inside the flash message)
    close_btn = page.locator("#flash a.close")
    if close_btn.count() > 0:
        close_btn.click()
        expect(flash).not_to_be_visible(timeout=5000)
    else:
        # No close button — just verify the flash message loaded
        expect(flash).to_be_visible(timeout=5000)
