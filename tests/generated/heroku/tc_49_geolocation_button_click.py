from pathlib import Path
from playwright.sync_api import Page, expect

BASE_URL = "https://the-internet.herokuapp.com/"
TEST_DATA_PATH = (
    Path(__file__).resolve().parent.parent.parent.parent
    / "config" / "test_data.json"
)


def test_geolocation_button_click(page: Page) -> None:
    page.goto("https://the-internet.herokuapp.com/geolocation")
    page.wait_for_load_state("domcontentloaded")

    # Mock geolocation via evaluate to avoid grant_permissions conflicts
    page.evaluate("""() => {
        navigator.geolocation.getCurrentPosition = function(success) {
            success({
                coords: {
                    latitude: 37.5665,
                    longitude: 126.9780,
                    accuracy: 1
                }
            });
        };
    }""")

    where_am_i_btn = page.get_by_role("button", name="Where am I?")
    expect(where_am_i_btn).to_be_visible(timeout=10000)
    where_am_i_btn.click()

    # Verify latitude and longitude appear in the page
    expect(page.locator("#lat-value")).to_be_visible(timeout=10000)
    expect(page.locator("#long-value")).to_be_visible(timeout=10000)
