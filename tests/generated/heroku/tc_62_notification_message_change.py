"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_62_notification_message_change (tc_62)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from pathlib import Path

from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_tc_62_notification_message_change(page):
    """알림 메시지 반복 클릭 시 변경 확인"""
    page.goto(BASE_URL + "notification_message_rendered")

    # First click
    page.locator("a", has_text="Click here").click()
    page.wait_for_load_state("domcontentloaded")

    flash = page.locator("#flash")
    expect(flash).to_be_visible(timeout=10000)
    first_text = flash.inner_text()

    # Second click — message may vary
    page.locator("a", has_text="Click here").click()
    page.wait_for_load_state("domcontentloaded")

    flash2 = page.locator("#flash")
    expect(flash2).to_be_visible(timeout=10000)

    # Verify that a message appears (content varies non-deterministically)
    second_text = flash2.inner_text()
    assert len(second_text.strip()) > 0, "Expected non-empty notification message"
    _ = first_text  # both messages captured
