import re
from playwright.sync_api import Page, expect

BASE_URL = "https://demoqa.com"


def test_homepage_widgets_card(page: Page):
    page.goto(BASE_URL + "/", wait_until="domcontentloaded")
    page.wait_for_timeout(2000)

    page.get_by_text("Widgets").first.click()
    page.wait_for_load_state("domcontentloaded")
    page.wait_for_timeout(2000)

    expect(page).to_have_url(re.compile(r"/widgets"))
    expect(page.locator(".left-pannel")).to_be_visible(timeout=10000)
    expect(page.locator(".left-pannel")).to_contain_text("Accordian", timeout=5000)
