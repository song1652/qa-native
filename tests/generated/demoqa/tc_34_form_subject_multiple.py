from playwright.sync_api import Page, expect

BASE_URL = "https://demoqa.com"


def test_form_subject_multiple_tags(page: Page):
    page.goto(f"{BASE_URL}/automation-practice-form", wait_until="domcontentloaded")
    page.wait_for_timeout(2000)

    # Remove ads/overlays
    page.evaluate(
        "document.querySelectorAll('ins.adsbygoogle, iframe[src*=google], "
        "iframe[src*=doubleclick], #fixedban, footer').forEach(e => e.remove())"
    )

    subjects_input = page.locator("#subjectsInput")

    # Add first subject: Maths
    subjects_input.click()
    subjects_input.type("Maths")
    page.wait_for_timeout(1000)
    page.locator(".subjects-auto-complete__option", has_text="Maths").first.click()
    page.wait_for_timeout(500)

    # Add second subject: Physics
    subjects_input.click()
    subjects_input.type("Physics")
    page.wait_for_timeout(1000)
    page.locator(".subjects-auto-complete__option", has_text="Physics").first.click()

    # Both tags should be visible
    tags = page.locator(".subjects-auto-complete__multi-value__label")
    expect(tags.filter(has_text="Maths")).to_be_visible(timeout=5000)
    expect(tags.filter(has_text="Physics")).to_be_visible(timeout=5000)
