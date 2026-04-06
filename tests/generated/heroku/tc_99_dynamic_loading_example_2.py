"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/dynamic_loading/2
케이스: tc_99_dynamic_loading_example_2 (tc_99)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com"


def test_tc_99_dynamic_loading_example_2(page):
    """Dynamic Loading Example 2 렌더링 후 표시"""
    page.goto(f"{BASE_URL}/dynamic_loading/2")
    page.wait_for_load_state("networkidle")

    page.locator("#start button").click()

    # Example 2: element is rendered into DOM after loading
    finish = page.locator("#finish")
    expect(finish).to_be_visible(timeout=10000)
    expect(finish).to_contain_text("Hello World!")
