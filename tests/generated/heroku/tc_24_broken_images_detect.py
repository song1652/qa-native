from pathlib import Path
from playwright.sync_api import Page, expect

BASE_URL = "https://the-internet.herokuapp.com/"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"


def test_broken_images_detect(page: Page):
    page.goto("https://the-internet.herokuapp.com/broken_images")
    page.wait_for_load_state("domcontentloaded")

    content = page.locator("div.example")
    expect(content).to_be_visible(timeout=10000)

    img_count = page.evaluate("() => document.querySelectorAll('div.example img').length")
    assert img_count >= 3, f"Expected at least 3 images, found {img_count}"

    broken_count = page.evaluate(
        "() => Array.from(document.querySelectorAll('div.example img')).filter(img => img.naturalWidth === 0).length"
    )
    assert broken_count > 0, "Expected at least one broken image (naturalWidth === 0)"
