import pytest
from playwright.sync_api import Page, expect

BASE_URL = "https://the-internet.herokuapp.com/"


def test_shifting_content_image_position(page: Page):
    page.goto("https://the-internet.herokuapp.com/shifting_content/image")
    page.wait_for_load_state("domcontentloaded")

    # Use scoped selector to avoid strict mode violation (page has 2 img elements)
    img = page.locator("#content img.shift")
    expect(img).to_be_visible(timeout=10000)

    box_before = img.bounding_box()
    assert box_before is not None

    page.reload()
    page.wait_for_load_state("domcontentloaded")

    img_after = page.locator("#content img.shift")
    expect(img_after).to_be_visible(timeout=10000)
