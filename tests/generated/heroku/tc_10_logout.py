"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_10_logout (tc_10)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
import json
from pathlib import Path

BASE_URL = "https://the-internet.herokuapp.com/"
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_tc_10_logout(page):
    """로그인 성공 후 Logout 버튼 클릭 시 /login으로 리다이렉트되고 로그아웃 flash 메시지 표시"""
    td = json.loads(TEST_DATA_PATH.read_text(encoding="utf-8"))
    user = td["heroku"]["valid_user"]

    page.goto("https://the-internet.herokuapp.com/login")
    page.locator("#username").fill(user["username"])
    page.locator("#password").fill(user["password"])
    page.locator("button.radius").click()
    page.wait_for_url("**/secure**", timeout=10000)

    logout_btn = page.locator('a[href="/logout"]')
    logout_btn.wait_for(state="visible", timeout=5000)
    logout_btn.click()

    page.wait_for_url("**/login**", timeout=10000)
    assert "/login" in page.url
    flash = page.locator("#flash")
    assert flash.is_visible()
    assert "logged out" in flash.inner_text().lower()
