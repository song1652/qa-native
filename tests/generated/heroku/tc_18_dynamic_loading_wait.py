"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: test_dynamic_loading_wait (tc_18)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"


def test_dynamic_loading_wait(page):
    """Dynamic Loading 요소 대기 — Start 클릭 후 Hello World! 표시 확인"""
    page.goto(BASE_URL + "dynamic_loading/1")

    page.locator("button", has_text="Start").click()

    expect(page.locator("#finish")).to_be_visible(timeout=15000)
    expect(page.locator("#finish")).to_contain_text("Hello World!", timeout=5000)
