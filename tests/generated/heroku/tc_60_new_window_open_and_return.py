import re
from pathlib import Path
from playwright.sync_api import Page, expect

BASE_URL = "https://the-internet.herokuapp.com/"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"


def test_new_window_open_and_return(page: Page) -> None:
    page.goto("https://the-internet.herokuapp.com/windows")
    page.wait_for_load_state("domcontentloaded")

    with page.context.expect_page() as new_page_info:
        page.locator("a", has_text="Click Here").click()

    new_page = new_page_info.value
    new_page.wait_for_load_state("domcontentloaded")
    expect(new_page.locator("body")).to_be_visible(timeout=10000)

    new_page.close()

    expect(page.locator("h3")).to_contain_text("Opening a new window", timeout=10000)
    expect(page).to_have_url(re.compile(r"/windows"))
