"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_57_large_dom_specific_cell (tc_57)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_tc_57_large_dom_specific_cell(page):
    """대규모 DOM 테이블의 특정 셀(row 50, col 1) 접근 및 50.1 텍스트 확인"""
    page.goto("https://the-internet.herokuapp.com/large")
    page.wait_for_load_state("domcontentloaded")

    page.wait_for_selector("#large-table", timeout=15000)

    # Row 50, column 1 — table rows are 1-indexed in CSS nth-child
    cell = page.locator("#large-table tr:nth-child(50) td:nth-child(1)")
    expect(cell).to_be_visible(timeout=10000)
    expect(cell).to_have_text("50.1", timeout=5000)
