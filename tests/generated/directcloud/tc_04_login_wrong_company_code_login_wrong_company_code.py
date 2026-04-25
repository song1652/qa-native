"""
자동 생성된 Playwright 테스트 코드
URL: https://web.directcloud.jp/login
케이스: tc_04_login_wrong_company_code (tc_04_login_wrong_company_code)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
import json
from pathlib import Path

BASE_URL = "https://web.directcloud.jp/login"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_tc_04_login_wrong_company_code(page):
    """존재하지 않는 회사코드로 로그인 실패"""
    with open(TEST_DATA_PATH, 'r', encoding='utf-8') as f:
        test_data = json.load(f)

    creds = test_data["directcloud"]["wrong_company"]
    page.goto(BASE_URL)
    page.fill('[name="company_code"]', creds["company"])
    page.fill('[name="id"]', creds["username"])
    page.fill('[name="password"]', creds["password"])
    page.click('#new_btn_login')
    page.wait_for_timeout(3000)

    assert "/login" in page.url
    assert "mybox" not in page.url
