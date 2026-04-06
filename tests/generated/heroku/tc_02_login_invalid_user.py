import json
from pathlib import Path
from playwright.sync_api import Page, expect

BASE_URL = "https://the-internet.herokuapp.com/"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"


def test_login_invalid_user(page: Page) -> None:
    with open(TEST_DATA_PATH) as f:
        test_data = json.load(f)

    username = test_data["heroku"]["invalid_user"]["username"]
    password = test_data["heroku"]["invalid_user"]["password"]

    page.goto("https://the-internet.herokuapp.com/login")
    page.wait_for_load_state("domcontentloaded")

    page.get_by_label("Username").fill(username)
    page.get_by_label("Password").fill(password)
    page.get_by_role("button", name="Login").click()

    expect(page).to_have_url("https://the-internet.herokuapp.com/login")
    expect(page.locator("#flash")).to_contain_text("Your username is invalid!")
