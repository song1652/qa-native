"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_100_dynamic_loading_indicator_wait (tc_100)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"


def test_tc_100_dynamic_loading_indicator_wait(page):
    """Start 클릭 후 로딩 바 표시 → 사라짐 → Hello World! 표시 순서 확인"""
    page.goto(BASE_URL + "dynamic_loading/1")
    page.wait_for_load_state("domcontentloaded")
    page.locator("#start button").click()
    expect(page.locator("#loading")).to_be_visible(timeout=5000)
    expect(page.locator("#finish")).to_be_visible(timeout=15000)
    expect(page.locator("#loading")).to_be_hidden(timeout=15000)
    expect(page.locator("#finish")).to_contain_text("Hello World!", timeout=5000)
