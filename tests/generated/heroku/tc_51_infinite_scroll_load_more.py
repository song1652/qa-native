from pathlib import Path
from playwright.sync_api import Page

BASE_URL = "https://the-internet.herokuapp.com/"
TEST_DATA_PATH = (
    Path(__file__).resolve().parent.parent.parent.parent
    / "config" / "test_data.json"
)


def test_infinite_scroll_load_more(page: Page) -> None:
    page.goto("https://the-internet.herokuapp.com/infinite_scroll")
    page.wait_for_load_state("domcontentloaded")

    page.wait_for_selector(".jscroll-added", timeout=10000)

    initial_count = page.locator(".jscroll-added").count()

    # Scroll to bottom to trigger infinite scroll
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(2000)

    new_count = page.locator(".jscroll-added").count()
    assert new_count > initial_count, (
        f"Expected more content blocks after scroll, "
        f"initial: {initial_count}, after scroll: {new_count}"
    )
