from playwright.sync_api import Page, expect

BASE_URL = "https://demoqa.com"


def test_accordian_third_section_opens_on_click(page: Page):
    page.goto(f"{BASE_URL}/accordian")
    page.wait_for_load_state("domcontentloaded")
    page.wait_for_timeout(2000)

    # Remove ads/overlays
    page.evaluate(
        "document.querySelectorAll('ins.adsbygoogle, iframe[src*=google], "
        "iframe[src*=doubleclick], #fixedban, footer').forEach(e => e.remove())"
    )

    third_item = page.locator(".accordion-item").nth(2)
    third_button = third_item.locator(".accordion-button")

    # Verify third section header text
    expect(third_button).to_contain_text("Why do we use it?")

    # Click third section to open it
    third_button.click()
    page.wait_for_timeout(500)

    # Third section body should be visible
    third_body = third_item.locator(".accordion-body")
    expect(third_body).to_be_visible(timeout=10000)

    third_body_text = third_body.inner_text()
    assert len(third_body_text) > 0, "Third accordion body should have visible content"

    # Third button should NOT have 'collapsed' class (meaning it's open)
    third_button_class = third_button.get_attribute("class") or ""
    assert "collapsed" not in third_button_class, "Third accordion section should be open after clicking"
