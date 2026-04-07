"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_99_dynamic_loading_example_2 (tc_99)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"


def test_tc_99_dynamic_loading_example_2(page):
    """Dynamic Loading Example 2: DOM에 새로 렌더링, Hello World! 확인"""
    page.goto("https://the-internet.herokuapp.com/dynamic_loading/2")
    page.wait_for_load_state("domcontentloaded")

    # Element does not exist in DOM yet
    page.locator("#start button").click()

    # Wait for element to be rendered and visible
    finish = page.locator("#finish")
    expect(finish).to_be_visible(timeout=15000)
    expect(finish).to_contain_text("Hello World!")
