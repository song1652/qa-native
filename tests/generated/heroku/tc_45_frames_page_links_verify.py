from pathlib import Path
from playwright.sync_api import Page, expect

BASE_URL = "https://the-internet.herokuapp.com/"
TEST_DATA_PATH = (
    Path(__file__).resolve().parent.parent.parent.parent
    / "config" / "test_data.json"
)


def test_frames_page_links_verify(page: Page) -> None:
    page.goto("https://the-internet.herokuapp.com/frames")
    page.wait_for_load_state("domcontentloaded")

    nested_link = page.get_by_role("link", name="Nested Frames")
    iframe_link = page.get_by_role("link", name="iFrame")

    expect(nested_link).to_be_visible(timeout=10000)
    expect(iframe_link).to_be_visible(timeout=10000)
