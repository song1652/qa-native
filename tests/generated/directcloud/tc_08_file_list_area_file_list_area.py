"""DirectCloud: tc_08 - 파일/폴더 목록 영역 확인"""
import json
from pathlib import Path

BASE_URL = "https://web.directcloud.jp/login"
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def login(page, company_code, user_id, password):
    page.goto(BASE_URL)
    page.wait_for_timeout(1000)
    page.fill('[name="company_code"]', company_code)
    page.fill('[name="id"]', user_id)
    page.fill('[name="password"]', password)
    page.click('#new_btn_login')
    try:
        page.wait_for_url("**/mybox/**", timeout=20000)
    except Exception:
        page.goto(BASE_URL)
        page.wait_for_timeout(3000)
        page.fill('[name="company_code"]', company_code)
        page.fill('[name="id"]', user_id)
        page.fill('[name="password"]', password)
        page.click('#new_btn_login')
        page.wait_for_url("**/mybox/**", timeout=20000)


def test_tc_08_file_list_area(page):
    """로그인 후 파일/폴더 목록 영역 확인"""
    with open(TEST_DATA_PATH, 'r', encoding='utf-8') as f:
        test_data = json.load(f)
    creds = test_data["directcloud"]["valid_user"]
    login(page, creds["company"], creds["username"], creds["password"])

    assert "mybox" in page.url
    # 페이지 로드 확인 (파일 목록 영역)
    page.wait_for_load_state('networkidle')
    assert page.locator('ul.table-files').is_visible(), "파일 목록 영역(ul.table-files)이 표시되지 않습니다"
    assert page.locator('li:has-text("My Box")').first.is_visible(), "MyBox 사이드바 메뉴가 표시되지 않습니다"
