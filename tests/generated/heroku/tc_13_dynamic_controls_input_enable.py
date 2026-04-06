"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_13_dynamic_controls_input_enable (tc_13)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from pathlib import Path

from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_dynamic_controls_input_enable(page):
    """Dynamic Controls 입력 필드 활성화"""
    page.goto(BASE_URL + "dynamic_controls")

    input_example = page.locator("#input-example")
    text_input = input_example.locator("input[type=text]")

    # Verify input is initially disabled
    expect(text_input).to_be_disabled()

    # Click Enable button
    input_example.locator("button").click()

    # Wait for "It's enabled!" message per lessons_learned
    expect(page.locator("#message")).to_contain_text("It's enabled!", timeout=15000)

    # Verify input is now enabled
    expect(text_input).to_be_enabled()
