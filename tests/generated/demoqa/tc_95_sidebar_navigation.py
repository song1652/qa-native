import re
from playwright.sync_api import Page, expect

BASE_URL = "https://demoqa.com"


def test_sidebar_navigation(page: Page):
    page.goto(BASE_URL + "/elements", wait_until="domcontentloaded")
    page.wait_for_timeout(2000)

    # Click Check Box in sidebar
    page.locator(".left-pannel").get_by_text("Check Box").click()
    page.wait_for_load_state("domcontentloaded")
    page.wait_for_timeout(2000)
    expect(page).to_have_url(re.compile(r"/checkbox"))
    # Header class is "text-center" not "main-header"
    expect(page.locator(".text-center")).to_contain_text("Check Box", timeout=5000)

    # Click Radio Button in sidebar
    page.locator(".left-pannel").get_by_text("Radio Button").click()
    page.wait_for_load_state("domcontentloaded")
    page.wait_for_timeout(2000)
    expect(page).to_have_url(re.compile(r"/radio-button"))
    expect(page.locator(".text-center")).to_contain_text("Radio Button", timeout=5000)

    # Click Web Tables in sidebar
    page.locator(".left-pannel").get_by_text("Web Tables").click()
    page.wait_for_load_state("domcontentloaded")
    page.wait_for_timeout(2000)
    expect(page).to_have_url(re.compile(r"/webtables"))
    expect(page.locator(".text-center")).to_contain_text("Web Tables", timeout=5000)
