from playwright.sync_api import Page, expect

BASE_URL = "https://demoqa.com"


def test_accordian_second_section_toggle_closes_first_section(page: Page):
    page.goto(f"{BASE_URL}/accordian")
    page.wait_for_load_state("domcontentloaded")
    page.wait_for_timeout(2000)

    # Remove ads/overlays
    page.evaluate(
        "document.querySelectorAll('ins.adsbygoogle, iframe[src*=google], "
        "iframe[src*=doubleclick], #fixedban, footer').forEach(e => e.remove())"
    )

    first_item = page.locator(".accordion-item").nth(0)
    second_item = page.locator(".accordion-item").nth(1)

    first_button = first_item.locator(".accordion-button")
    second_button = second_item.locator(".accordion-button")

    # Verify second section header text
    expect(second_button).to_contain_text("Where does it come from?")

    # Click second section to open it
    second_button.click()
    page.wait_for_timeout(500)

    # Second section body should be visible
    second_body = second_item.locator(".accordion-body")
    expect(second_body).to_be_visible(timeout=10000)

    second_body_text = second_body.inner_text()
    assert len(second_body_text) > 0, "Second accordion body should have visible content"

    # First section should now be collapsed (button has 'collapsed' class)
    first_button_class = first_button.get_attribute("class") or ""
    assert "collapsed" in first_button_class, "First accordion section should be closed after clicking second"
