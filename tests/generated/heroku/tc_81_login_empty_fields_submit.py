from pathlib import Path
from playwright.sync_api import Page, expect

BASE_URL = "https://the-internet.herokuapp.com/"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"


def test_login_empty_fields_submit(page: Page):
    page.goto("https://the-internet.herokuapp.com/login")
    page.wait_for_load_state("domcontentloaded")

    page.get_by_role("button", name="Login").click()

    expect(page.locator("#flash")).to_be_visible(timeout=10000)
    expect(page.locator("#flash")).to_contain_text("Your username is invalid!", timeout=5000)
