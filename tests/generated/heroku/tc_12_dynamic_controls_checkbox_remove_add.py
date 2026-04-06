"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_12_dynamic_controls_checkbox_remove_add (tc_12)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from pathlib import Path

from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_dynamic_controls_checkbox_remove_add(page):
    """Dynamic Controls 체크박스 제거/추가"""
    page.goto(BASE_URL + "dynamic_controls")

    # Use #checkbox-example per lessons_learned
    checkbox_example = page.locator("#checkbox-example")

    # Verify checkbox is initially visible
    expect(checkbox_example.locator("input[type=checkbox]")).to_be_visible()

    # Click Remove button
    checkbox_example.locator("button").click()

    # Wait for #message per lessons_learned (avoid #loading which has duplicates)
    expect(page.locator("#message")).to_contain_text("It's gone!", timeout=15000)

    # Verify checkbox is gone
    expect(checkbox_example.locator("input[type=checkbox]")).not_to_be_visible()

    # Click Add button
    checkbox_example.locator("button").click()

    # Wait for It's back! message
    expect(page.locator("#message")).to_contain_text("It's back!", timeout=15000)

    # Verify checkbox reappeared - use #checkbox-example input[type=checkbox] per lessons_learned
    expect(page.locator("#checkbox-example input[type=checkbox]")).to_be_visible()
