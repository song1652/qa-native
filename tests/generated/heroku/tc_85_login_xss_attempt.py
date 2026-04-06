"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_85_login_xss_attempt (tc_85)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from pathlib import Path

from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_tc_85_login_xss_attempt(page):
    """XSS 스크립트 로그인 시도"""
    # Register dialog handler to catch any unexpected alert — fail if one fires
    alert_fired = []

    def on_dialog(dialog):
        alert_fired.append(dialog.message)
        dialog.dismiss()

    page.on("dialog", on_dialog)

    page.goto(BASE_URL + "login")

    # Enter XSS payload as username
    page.locator("#username").fill("<script>alert(1)</script>")
    page.locator("#password").fill("test")
    page.locator("button.radius").click()

    # Login must fail, no alert should fire
    expect(page.locator("#flash-messages")).to_contain_text(
        "Your username is invalid!", timeout=10000
    )
    assert len(alert_fired) == 0, (
        f"Unexpected alert dialog fired: {alert_fired}"
    )
