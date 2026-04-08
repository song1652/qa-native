from playwright.sync_api import Page, expect

BASE_URL = "https://demoqa.com"


def test_accordian_first_section_is_open_by_default(page: Page):
    page.goto(f"{BASE_URL}/accordian")
    page.wait_for_load_state("domcontentloaded")
    page.wait_for_timeout(2000)

    # Remove ads/overlays
    page.evaluate(
        "document.querySelectorAll('ins.adsbygoogle, iframe[src*=google], "
        "iframe[src*=doubleclick], #fixedban, footer').forEach(e => e.remove())"
    )

    # First accordion item button should be visible and have 'What is Lorem Ipsum?' text
    first_button = page.locator(".accordion-item").nth(0).locator(".accordion-button")
    expect(first_button).to_be_visible(timeout=10000)
    expect(first_button).to_contain_text("What is Lorem Ipsum?")

    # The first section button should NOT have 'collapsed' class (meaning it's open)
    # Bootstrap 5: collapsed class is absent when open
    button_class = first_button.get_attribute("class") or ""
    assert "collapsed" not in button_class, "First accordion section should be open by default"

    # The accordion body for the first item should be visible
    first_body = page.locator(".accordion-item").nth(0).locator(".accordion-body")
    expect(first_body).to_be_visible(timeout=5000)

    body_text = first_body.inner_text()
    assert len(body_text) > 0, "First accordion body should have visible content"
