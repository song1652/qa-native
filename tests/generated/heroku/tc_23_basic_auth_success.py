"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_23_basic_auth_success (tc_23)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_tc_23_basic_auth_success(page):
    """Basic Auth 인증 성공"""
    # Use credentials embedded in URL for Basic Auth
    page.goto("https://admin:admin@the-internet.herokuapp.com/basic_auth")
    expect(page.locator("body")).to_be_visible()

    # Verify success message
    content = page.locator("#content")
    expect(content).to_be_visible(timeout=10000)
    expect(content).to_contain_text("Congratulations")
