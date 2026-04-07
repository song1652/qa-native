"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_94_add_remove_repeat (tc_94)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"


def test_tc_94_add_remove_repeat(page):
    """추가 2회 → 삭제 1회 → 추가 1회 후 Delete 버튼 2개 확인"""
    page.goto("https://the-internet.herokuapp.com/add_remove_elements/")
    page.wait_for_load_state("domcontentloaded")

    add_button = page.locator("button", has_text="Add Element")

    # Add 2 elements
    add_button.click()
    add_button.click()
    expect(page.locator("#elements button.added-manually")).to_have_count(2)

    # Remove 1 element
    page.locator("#elements button.added-manually").first.click()
    expect(page.locator("#elements button.added-manually")).to_have_count(1)

    # Add 1 more element
    add_button.click()
    expect(page.locator("#elements button.added-manually")).to_have_count(2)
