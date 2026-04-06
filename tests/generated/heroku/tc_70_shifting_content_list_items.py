import pytest
from playwright.sync_api import Page, expect

BASE_URL = "https://the-internet.herokuapp.com/"


def test_shifting_content_list_items(page: Page):
    page.goto("https://the-internet.herokuapp.com/shifting_content/list")
    page.wait_for_load_state("domcontentloaded")

    # lessons_learned: shifting_content/list uses <br><br> separated text, not <li> elements
    # Verify the content area has text entries (at least 1 row)
    content = page.locator("#content .row")
    expect(content.first).to_be_visible(timeout=10000)

    # Check that some content text is rendered in the content area
    content_text = page.locator("#content .large-6").inner_text()
    assert len(content_text.strip()) > 0, "Expected non-empty content in shifting list page"
