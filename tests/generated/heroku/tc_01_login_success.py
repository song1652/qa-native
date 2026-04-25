"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_01_login_success (tc_01)
"""
import json
from pathlib import Path

BASE_URL = "https://the-internet.herokuapp.com/"
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_tc_01_login_success(page):
    """유효한 자격증명으로 로그인 성공 후 /secure URL로 이동하고 flash 메시지가 표시된다"""
    td = json.loads(TEST_DATA_PATH.read_text(encoding="utf-8"))
    user = td["heroku"]["valid_user"]

    page.goto("https://the-internet.herokuapp.com/login")
    page.locator("#username").fill(user["username"])
    page.locator("#password").fill(user["password"])
    page.locator("button.radius").click()

    page.wait_for_url("**/secure**", timeout=10000)
    assert "/secure" in page.url
    assert page.locator("#flash").is_visible()
    assert "You logged into a secure area!" in page.locator("#flash").inner_text()
    assert page.locator('a[href="/logout"]').is_visible()
