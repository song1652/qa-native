from pathlib import Path
from playwright.sync_api import Page, expect

BASE_URL = "https://the-internet.herokuapp.com/"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"


def test_abtest_content_variation(page: Page):
    page.goto("https://the-internet.herokuapp.com/abtest")
    page.wait_for_load_state("domcontentloaded")

    heading = page.locator("h3")
    expect(heading).to_be_visible(timeout=10000)

    first_title = heading.inner_text()
    valid_titles = ["A/B Test Control", "A/B Test Variation 1"]
    assert first_title in valid_titles, f"Unexpected heading on first load: '{first_title}'"

    page.reload()
    page.wait_for_load_state("domcontentloaded")

    heading_after_reload = page.locator("h3")
    expect(heading_after_reload).to_be_visible(timeout=10000)

    second_title = heading_after_reload.inner_text()
    assert second_title in valid_titles, f"Unexpected heading after reload: '{second_title}'"

    example_div = page.locator("div.example")
    expect(example_div).to_be_visible(timeout=5000)
