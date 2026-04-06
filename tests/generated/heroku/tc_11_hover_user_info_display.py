from pathlib import Path
from playwright.sync_api import Page, expect

BASE_URL = "https://the-internet.herokuapp.com/"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"


def test_hover_user_info_display(page: Page):
    # hovers 페이지: 첫 번째 사용자 이미지 호버 시 정보 표시
    page.goto("https://the-internet.herokuapp.com/hovers")
    page.wait_for_load_state("domcontentloaded")

    # 첫 번째 figure에 hover (locator().nth() 패턴 사용 - lessons_learned 참조)
    figure = page.locator("div.figure").nth(0)
    figure.hover()

    # .figcaption CSS 클래스 사용 (figcaption 태그 아님 - lessons_learned 참조)
    caption = figure.locator(".figcaption")
    expect(caption).to_be_visible(timeout=5000)
    expect(caption).to_contain_text("name: user1", timeout=5000)
    expect(caption.locator("a")).to_be_visible(timeout=5000)
    expect(caption.locator("a")).to_contain_text("View profile", timeout=5000)
