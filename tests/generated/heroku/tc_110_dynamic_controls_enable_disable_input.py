"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_110_dynamic_controls_enable_disable_input (tc_110)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_tc_110_dynamic_controls_enable_disable_input(page):
    """입력 필드 disabled 확인 → Enable → enabled → Disable → disabled 전환 확인"""
    page.goto(BASE_URL + "dynamic_controls")
    page.wait_for_load_state("domcontentloaded")
    input_field = page.locator("#input-example input[type='text']")
    expect(input_field).to_be_disabled(timeout=5000)
    page.locator("#input-example button").click()
    expect(page.locator("#message")).to_contain_text("It's enabled!", timeout=10000)
    expect(input_field).to_be_enabled(timeout=10000)
    page.locator("#input-example button").click()
    expect(page.locator("#message")).to_contain_text("It's disabled!", timeout=10000)
    expect(input_field).to_be_disabled(timeout=10000)
