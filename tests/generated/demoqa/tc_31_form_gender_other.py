from playwright.sync_api import Page, expect

BASE_URL = "https://demoqa.com"


def test_form_gender_other(page: Page):
    page.goto(f"{BASE_URL}/automation-practice-form", wait_until="domcontentloaded")
    page.wait_for_timeout(2000)

    # Remove ads/overlays
    page.evaluate(
        "document.querySelectorAll('ins.adsbygoogle, iframe[src*=google], "
        "iframe[src*=doubleclick], #fixedban, footer').forEach(e => e.remove())"
    )

    # Radio buttons are visually hidden; click the label instead
    page.locator("label", has_text="Other").click()

    # Other radio should be checked
    expect(page.locator("input[value='Other']")).to_be_checked(timeout=5000)

    # Male and Female should NOT be checked
    expect(page.locator("input[value='Male']")).not_to_be_checked()
    expect(page.locator("input[value='Female']")).not_to_be_checked()
