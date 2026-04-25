"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_02_login_wrong_password (tc_02)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
import json
from pathlib import Path

BASE_URL = "https://the-internet.herokuapp.com/"
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_tc_02_login_wrong_password(page):
    """잘못된 자격증명으로 로그인 시 /login URL 유지 및 에러 flash 메시지 표시"""
    td = json.loads(TEST_DATA_PATH.read_text(encoding="utf-8"))
    user = td["heroku"]["invalid_user"]

    page.goto("https://the-internet.herokuapp.com/login")
    page.locator("#username").fill(user["username"])
    page.locator("#password").fill(user["password"])
    page.locator("button.radius").click()

    page.wait_for_load_state("networkidle")
    assert "/login" in page.url
    flash = page.locator("#flash")
    assert flash.is_visible()
    flash_text = flash.inner_text()
    assert "invalid" in flash_text.lower()
