"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/dynamic_loading/1
케이스: tc_100_dynamic_loading_indicator_wait (tc_100)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com"


def test_tc_100_dynamic_loading_indicator_wait(page):
    """Dynamic Loading 로딩 인디케이터 대기"""
    page.goto(f"{BASE_URL}/dynamic_loading/1")
    page.wait_for_load_state("networkidle")

    page.locator("#start button").click()

    # #loading appears during loading — wait for it to become hidden
    loading = page.locator("#loading")
    # Wait for loading to disappear (it may appear briefly)
    expect(loading).to_be_hidden(timeout=10000)

    # After loading disappears, #finish should be visible
    finish = page.locator("#finish")
    expect(finish).to_be_visible(timeout=5000)
    expect(finish).to_contain_text("Hello World!")
