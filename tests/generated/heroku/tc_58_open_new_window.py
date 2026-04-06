import re
from pathlib import Path
from playwright.sync_api import Page, expect

BASE_URL = "https://the-internet.herokuapp.com/"
TEST_DATA_PATH = (
    Path(__file__).resolve()
    .parent.parent.parent.parent
    / "config" / "test_data.json"
)


def test_open_new_window(page: Page):
    """새 창 열기"""
    page.goto("https://the-internet.herokuapp.com/windows")
    page.wait_for_load_state("domcontentloaded")

    with page.context.expect_page() as new_page_info:
        page.get_by_role("link", name="Click Here").click()

    new_page = new_page_info.value
    new_page.wait_for_load_state("domcontentloaded")

    expect(new_page).to_have_url(
        re.compile(r"/windows/new"), timeout=10000
    )
