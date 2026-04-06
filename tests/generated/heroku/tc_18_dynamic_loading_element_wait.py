"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_18_dynamic_loading_element_wait (tc_18)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_tc_18_dynamic_loading_element_wait(page):
    """Dynamic Loading 요소 대기"""
    page.goto(BASE_URL + "dynamic_loading/1")
    expect(page.locator("body")).to_be_visible()

    # Click Start button
    page.locator("#start button").click()

    # Wait for loading indicator to disappear
    page.locator("#loading").wait_for(state="hidden", timeout=15000)

    # Verify finish text
    finish = page.locator("#finish")
    expect(finish).to_be_visible(timeout=10000)
    expect(finish).to_contain_text("Hello World!")
