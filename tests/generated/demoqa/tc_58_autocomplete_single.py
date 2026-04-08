from playwright.sync_api import Page, expect

BASE_URL = "https://demoqa.com"


def test_auto_complete_single_color_selection_shows_value(page: Page):
    page.goto(f"{BASE_URL}/auto-complete")
    page.wait_for_load_state("domcontentloaded")
    page.wait_for_timeout(2000)

    # Remove ads/overlays
    page.evaluate(
        "document.querySelectorAll('ins.adsbygoogle, iframe[src*=google], "
        "iframe[src*=doubleclick], #fixedban, footer').forEach(e => e.remove())"
    )

    # Type in single-value autocomplete field
    single_input = page.locator("#autoCompleteSingleInput")
    single_input.click()
    single_input.type("Gr")
    page.wait_for_timeout(500)

    # Select 'Green' from dropdown
    green_option = page.locator(".auto-complete__menu-list .auto-complete__option", has_text="Green")
    expect(green_option).to_be_visible(timeout=5000)
    green_option.click()
    page.wait_for_timeout(300)

    # Verify 'Green' is shown in the single field container
    single_container = page.locator("#autoCompleteSingleContainer")
    expect(single_container).to_contain_text("Green")
