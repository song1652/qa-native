"""
자동 생성된 Playwright 테스트 코드
URL: https://web.directcloud.jp/login
케이스: tc_06_forgot_password_button (tc_06_forgot_password_button)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from pathlib import Path

BASE_URL = "https://web.directcloud.jp/login"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_tc_06_forgot_password_button(page):
    """Forgot Password 버튼 동작 확인"""
    page.goto(BASE_URL)

    forgot_btn = page.locator('button:has-text("Forgot")')
    assert forgot_btn.first.is_visible()

    forgot_btn.first.click()
    page.wait_for_timeout(2000)

    assert page.locator('[name="company_code"]').is_visible(), "비밀번호 찾기 후 로그인 페이지가 표시되지 않습니다"
