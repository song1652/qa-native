"""
자동 생성된 Playwright 테스트 코드
URL: https://web.directcloud.jp/login
케이스: tc_01_login_success (정상 로그인 성공)
"""
import json
from pathlib import Path

BASE_URL = "https://web.directcloud.jp/login"
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_tc_01_login_success(page):
    """정상 로그인 성공"""
    with open(str(TEST_DATA_PATH), 'r', encoding='utf-8') as f:
        test_data = json.load(f)

    user = test_data['directcloud']['valid_user']

    page.goto(BASE_URL)
    page.fill('[name="company_code"]', user['company'])
    page.fill('[name="id"]', user['username'])
    page.fill('[name="password"]', user['password'])
    page.click('#new_btn_login')
    try:
        page.wait_for_url("**/mybox/**", timeout=20000)
    except Exception:
        # 세션 충돌 또는 dialog 수락 후 retry
        page.goto(BASE_URL)
        page.wait_for_timeout(3000)
        page.fill('[name="company_code"]', user['company'])
        page.fill('[name="id"]', user['username'])
        page.fill('[name="password"]', user['password'])
        page.click('#new_btn_login')
        page.wait_for_url("**/mybox/**", timeout=20000)
    page.wait_for_timeout(1500)
    # 검색창 또는 사이드바로 로그인 성공 확인
    assert (
        page.locator('[placeholder="검색"]').count() > 0
        or page.locator('li:has-text("My Box")').count() > 0
    ), "로그인 후 검색창 또는 MyBox 사이드바가 표시되지 않습니다"
