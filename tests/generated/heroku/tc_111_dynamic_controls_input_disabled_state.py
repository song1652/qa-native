"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_111_dynamic_controls_input_disabled_state (tc_111)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_tc_111_dynamic_controls_input_disabled_state(page):
    """비활성화 상태에서 입력 필드 disabled 속성 확인"""
    page.goto(BASE_URL + "dynamic_controls")
    page.wait_for_load_state("domcontentloaded")
    input_field = page.locator("#input-example input[type='text']")
    expect(input_field).to_be_visible(timeout=5000)
    expect(input_field).to_be_disabled(timeout=5000)
