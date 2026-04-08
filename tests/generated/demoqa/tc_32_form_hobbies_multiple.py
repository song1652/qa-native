from playwright.sync_api import Page, expect

BASE_URL = "https://demoqa.com"


def test_form_hobbies_multiple(page: Page):
    page.goto(f"{BASE_URL}/automation-practice-form", wait_until="domcontentloaded")
    page.wait_for_timeout(2000)

    # Remove ads/overlays
    page.evaluate(
        "document.querySelectorAll('ins.adsbygoogle, iframe[src*=google], "
        "iframe[src*=doubleclick], #fixedban, footer').forEach(e => e.remove())"
    )

    # Checkboxes are visually hidden; click their labels by for attribute
    page.locator("label[for='hobbies-checkbox-1']").click()  # Sports
    page.locator("label[for='hobbies-checkbox-2']").click()  # Reading
    page.locator("label[for='hobbies-checkbox-3']").click()  # Music

    # All three checkboxes should be checked
    expect(page.locator("#hobbies-checkbox-1")).to_be_checked(timeout=5000)
    expect(page.locator("#hobbies-checkbox-2")).to_be_checked(timeout=5000)
    expect(page.locator("#hobbies-checkbox-3")).to_be_checked(timeout=5000)
