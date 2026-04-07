"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_101_table_sort_last_name (tc_101)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
import re
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_tc_101_table_sort_last_name(page):
    """테이블1 Last Name 헤더 클릭 후 headerSortDown 클래스 적용 확인 (첫 클릭=내림차순)"""
    page.goto("https://the-internet.herokuapp.com/tables")
    page.wait_for_load_state("domcontentloaded")
    th = page.locator("#table1 thead th").nth(0)
    th.click()
    page.wait_for_timeout(300)
    expect(th).to_have_class(re.compile(r"headerSortDown"))
