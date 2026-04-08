from playwright.sync_api import Page, expect

BASE_URL = "https://demoqa.com"


def test_auto_complete_multi_color_selection_shows_tags(page: Page):
    page.goto(f"{BASE_URL}/auto-complete")
    page.wait_for_load_state("domcontentloaded")
    page.wait_for_timeout(2000)

    # Remove ads/overlays
    page.evaluate(
        "document.querySelectorAll('ins.adsbygoogle, iframe[src*=google], "
        "iframe[src*=doubleclick], #fixedban, footer').forEach(e => e.remove())"
    )

    # Type in the multi-value autocomplete field
    multi_input = page.locator("#autoCompleteMultipleInput")
    multi_input.click()
    multi_input.type("Re")
    page.wait_for_timeout(500)

    # Select 'Red' from dropdown
    red_option = page.locator(".auto-complete__menu-list .auto-complete__option", has_text="Red")
    expect(red_option).to_be_visible(timeout=5000)
    red_option.click()
    page.wait_for_timeout(300)

    # Type 'Bl' and select Blue
    multi_input.type("Bl")
    page.wait_for_timeout(500)

    blue_option = page.locator(".auto-complete__menu-list .auto-complete__option", has_text="Blue")
    expect(blue_option).to_be_visible(timeout=5000)
    blue_option.click()
    page.wait_for_timeout(300)

    # Verify both Red and Blue tags are shown
    tags_container = page.locator("#autoCompleteMultipleContainer")
    expect(tags_container).to_contain_text("Red")
    expect(tags_container).to_contain_text("Blue")
