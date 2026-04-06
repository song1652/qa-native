import json
from pathlib import Path
from playwright.sync_api import Page, expect

BASE_URL = "https://the-internet.herokuapp.com/"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"


def test_hover_user2_profile(page: Page):
    """tc_96: 유저 2 프로필 호버 - 두 번째 이미지 호버 시 name: user2 및 View profile 표시"""
    page.goto("https://the-internet.herokuapp.com/hovers")
    page.wait_for_load_state("domcontentloaded")

    # lessons_learned: locator().nth(N).hover() 패턴 사용, .figcaption CSS 클래스
    figure = page.locator("div.figure").nth(1)
    expect(figure).to_be_visible(timeout=10000)

    figure.hover()

    caption = figure.locator(".figcaption")
    expect(caption).to_be_visible(timeout=5000)
    expect(caption).to_contain_text("name: user2", timeout=5000)
    expect(caption.get_by_role("link", name="View profile")).to_be_visible(timeout=5000)
