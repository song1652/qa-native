from pathlib import Path
from playwright.sync_api import Page, expect

BASE_URL = "https://the-internet.herokuapp.com/"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"


def test_basic_auth_success(page: Page):
    page.goto("https://admin:admin@the-internet.herokuapp.com/basic_auth")
    page.wait_for_load_state("domcontentloaded")

    content = page.locator("div.example")
    expect(content).to_be_visible(timeout=10000)

    expect(content).to_contain_text("Congratulations", timeout=5000)
