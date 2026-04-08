"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_109_dynamic_controls_remove_and_add_checkbox (tc_109)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_tc_109_dynamic_controls_remove_and_add_checkbox(page):
    """체크박스 존재 확인 → Remove → 사라짐 → Add → 재표시 확인 (#checkbox-example input[type=checkbox])"""
    page.goto(BASE_URL + "dynamic_controls")
    page.wait_for_load_state("domcontentloaded")
    checkbox = page.locator("#checkbox-example input[type=checkbox]")
    expect(checkbox).to_be_visible(timeout=5000)
    page.locator("#checkbox-example button").click()
    expect(page.locator("#message")).to_be_visible(timeout=10000)
    expect(checkbox).to_be_hidden(timeout=5000)
    page.locator("#checkbox-example button").click()
    expect(page.locator("#message")).to_be_visible(timeout=10000)
    expect(page.locator("#checkbox-example input[type=checkbox]")).to_be_visible(timeout=10000)
