from playwright.sync_api import Page, expect

BASE_URL = "https://demoqa.com"


def test_sidebar_expand_collapse(page: Page):
    page.goto(BASE_URL + "/elements", wait_until="domcontentloaded")
    page.wait_for_timeout(2000)

    # Find the Widgets group header in the sidebar
    widgets_header = page.locator(".left-pannel").get_by_text("Widgets")

    # Click to expand
    widgets_header.click()
    page.wait_for_timeout(1000)

    # Verify sub-menu items are visible (e.g., Accordian)
    accordian_link = page.locator(".left-pannel").get_by_text("Accordian")
    expect(accordian_link).to_be_visible(timeout=5000)

    # Click again to collapse
    widgets_header.click()
    page.wait_for_timeout(1000)

    # Verify sub-menu is hidden
    expect(accordian_link).to_be_hidden(timeout=5000)
