import re
import json
from pathlib import Path
from playwright.sync_api import Page, expect

BASE_URL = "https://the-internet.herokuapp.com/"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"


def test_hover_user3_view_profile_link(page: Page):
    """tc_97: 유저 3 호버 후 프로필 링크 확인 - 호버 시 name: user3, 클릭 시 /users/3 이동"""
    page.goto("https://the-internet.herokuapp.com/hovers")
    page.wait_for_load_state("domcontentloaded")

    # lessons_learned: locator().nth(N).hover() 패턴 사용, .figcaption CSS 클래스
    figure = page.locator("div.figure").nth(2)
    expect(figure).to_be_visible(timeout=10000)

    figure.hover()

    caption = figure.locator(".figcaption")
    expect(caption).to_be_visible(timeout=5000)
    expect(caption).to_contain_text("name: user3", timeout=5000)

    view_profile_link = caption.get_by_role("link", name="View profile")
    expect(view_profile_link).to_be_visible(timeout=5000)

    view_profile_link.click()
    page.wait_for_load_state("domcontentloaded")

    expect(page).to_have_url(re.compile(r"/users/3"), timeout=10000)
