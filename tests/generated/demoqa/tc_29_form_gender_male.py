from playwright.sync_api import Page, expect

BASE_URL = "https://demoqa.com"


def test_form_gender_male(page: Page):
    page.goto(f"{BASE_URL}/automation-practice-form", wait_until="domcontentloaded")
    page.wait_for_timeout(2000)

    # Remove ads/overlays
    page.evaluate(
        "document.querySelectorAll('ins.adsbygoogle, iframe[src*=google], "
        "iframe[src*=doubleclick], #fixedban, footer').forEach(e => e.remove())"
    )

    # Radio buttons are visually hidden; click the label by for attribute to avoid strict mode
    page.locator("label[for='gender-radio-1']").click()

    # Male radio should be checked
    male_radio = page.locator("#gender-radio-1")
    expect(male_radio).to_be_checked(timeout=5000)

    # Female and Other should NOT be checked
    expect(page.locator("#gender-radio-2")).not_to_be_checked()
    expect(page.locator("#gender-radio-3")).not_to_be_checked()
