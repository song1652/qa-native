"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_08_js_confirm_accept (tc_08)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from pathlib import Path

from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_js_confirm_accept(page):
    """JS Confirm 수락"""
    page.goto(BASE_URL + "javascript_alerts")

    # Set up dialog handler to accept
    page.on("dialog", lambda dialog: dialog.accept())

    page.locator("button", has_text="Click for JS Confirm").click()

    expect(page.locator("#result")).to_contain_text(
        "You clicked: Ok", timeout=10000
    )
