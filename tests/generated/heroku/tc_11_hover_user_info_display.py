"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_11_hover_user_info_display (tc_11)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from pathlib import Path

from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_hover_user_info_display(page):
    """호버 시 사용자 정보 표시"""
    page.goto(BASE_URL + "hovers")

    # Hover over first figure using locator().hover() per lessons_learned
    page.locator("div.figure").nth(0).hover()

    # figcaption is a CSS class per lessons_learned (not <figcaption> tag)
    figcaption = page.locator("div.figure").nth(0).locator(".figcaption")
    expect(figcaption).to_be_visible(timeout=10000)
    expect(figcaption).to_contain_text("name: user1")
    expect(figcaption.locator("a")).to_be_visible()
