from pathlib import Path
from playwright.sync_api import Page, expect

BASE_URL = "https://the-internet.herokuapp.com/"
TEST_DATA_PATH = (
    Path(__file__).resolve().parent.parent.parent.parent
    / "config" / "test_data.json"
)


def test_iframe_access_and_content_verify(page: Page) -> None:
    page.goto("https://the-internet.herokuapp.com/frames")
    page.wait_for_load_state("domcontentloaded")

    page.get_by_role("link", name="iFrame").click()
    page.wait_for_load_state("domcontentloaded")

    expect(page).to_have_url("https://the-internet.herokuapp.com/iframe")

    iframe_el = page.locator("iframe#mce_0_ifr")
    expect(iframe_el).to_be_visible(timeout=10000)
