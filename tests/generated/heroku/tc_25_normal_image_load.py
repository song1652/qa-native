from pathlib import Path
from playwright.sync_api import Page, expect

BASE_URL = "https://the-internet.herokuapp.com/"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"


def test_normal_image_load(page: Page):
    page.goto("https://the-internet.herokuapp.com/broken_images")
    page.wait_for_load_state("domcontentloaded")

    content = page.locator("div.example")
    expect(content).to_be_visible(timeout=10000)

    loaded_count = page.evaluate(
        "() => Array.from(document.querySelectorAll('div.example img')).filter(img => img.naturalWidth > 0).length"
    )
    assert loaded_count >= 1, f"Expected at least 1 normally loaded image, found {loaded_count}"
