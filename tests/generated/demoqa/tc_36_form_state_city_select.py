from playwright.sync_api import Page, expect

BASE_URL = "https://demoqa.com"

AD_REMOVE_JS = (
    "document.querySelectorAll("
    "'ins.adsbygoogle, iframe[src*=google], iframe[src*=doubleclick], #fixedban, footer'"
    ").forEach(e => e.remove())"
)


def test_form_state_city_select(page: Page):
    page.goto(f"{BASE_URL}/automation-practice-form")
    page.wait_for_load_state("domcontentloaded")
    page.wait_for_timeout(2000)

    # Remove ads/overlays
    page.evaluate(AD_REMOVE_JS)

    # Click State react-select container
    state_container = page.locator("#state")
    state_container.click()
    page.wait_for_timeout(500)

    # Select NCR option
    page.get_by_text("NCR", exact=True).click()
    page.wait_for_timeout(500)

    # Verify State shows NCR
    expect(state_container).to_contain_text("NCR")

    # Click City react-select container
    city_container = page.locator("#city")
    city_container.click()
    page.wait_for_timeout(500)

    # Select Delhi option
    page.get_by_text("Delhi", exact=True).click()
    page.wait_for_timeout(500)

    # Verify City shows Delhi
    expect(city_container).to_contain_text("Delhi")
