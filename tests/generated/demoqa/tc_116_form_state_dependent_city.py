from pathlib import Path
from playwright.sync_api import Page, expect

BASE_URL = "https://demoqa.com"
TEST_DATA_PATH = (
    Path(__file__).resolve().parent.parent.parent.parent
    / "config" / "test_data.json"
)


def test_form_state_dependent_city_options(page: Page):
    page.goto(f"{BASE_URL}/automation-practice-form")
    page.wait_for_load_state("domcontentloaded")
    page.wait_for_timeout(2000)

    # Remove ads/overlays
    page.evaluate(
        "document.querySelectorAll("
        "'ins.adsbygoogle, iframe[src*=google],"
        " iframe[src*=doubleclick], #fixedban, footer'"
        ").forEach(e => e.remove())"
    )

    # Scroll down to State field
    state_container = page.locator("#state")
    state_container.scroll_into_view_if_needed()
    page.wait_for_timeout(500)

    # Click State dropdown
    state_container.click()
    page.wait_for_timeout(500)

    # Select "Uttar Pradesh"
    option = (
        page.locator("[class*='option']")
        .filter(has_text="Uttar Pradesh")
        .first
    )
    expect(option).to_be_visible(timeout=5000)
    option.click()
    page.wait_for_timeout(500)

    # Click City dropdown
    city_container = page.locator("#city")
    city_container.click()
    page.wait_for_timeout(500)

    # Verify Uttar Pradesh cities appear in menu
    menu = page.locator("[class*='menu']").last
    expect(menu).to_be_visible(timeout=5000)
    menu_text = menu.inner_text()
    has_city = (
        "Agra" in menu_text
        or "Lucknow" in menu_text
        or "Merrut" in menu_text
    )
    assert has_city, f"Expected UP cities in menu, got: {menu_text}"
