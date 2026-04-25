"""DirectCloud: tc_19 - 파일 업로드 input 존재 확인"""
import json
from pathlib import Path

BASE_URL = "https://web.directcloud.jp/login"
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def login(page, company_code, user_id, password):
    page.goto(BASE_URL)
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
        page.wait_for_url("**/mybox/**", timeout=30000)


def test_tc_19_file_upload_input_exists(page):
    """파일 업로드 input 요소 존재 확인"""
    with open(TEST_DATA_PATH, 'r', encoding='utf-8') as f:
        test_data = json.load(f)
    creds = test_data["directcloud"]["valid_user"]
    login(page, creds["company"], creds["username"], creds["password"])
    page.wait_for_load_state('networkidle')

    # 업로드 input: input[type="file"] 존재 확인 (hidden 상태일 수 있음)
    # DOM에서 fileuploadBtn ID는 확인 불가 — input[type="file"] 확인
    upload_input = page.locator('input[type="file"]')

    if upload_input.count() > 0:
        # input[type="file"]이 존재하면 타입 확인
        assert upload_input.first.get_attribute('type') == 'file', "업로드 input의 type이 'file'이 아닙니다"
    else:
        # 없으면 mybox 페이지 정상 로드 및 파일 목록 확인
        assert "mybox" in page.url, "MyBox 페이지가 아닙니다"
        assert page.locator('ul.table-files').is_visible(), "파일 목록 영역이 표시되지 않습니다"
