from playwright.sync_api import Page, expect

BASE_URL = "https://demoqa.com"


def test_form_subject_autocomplete(page: Page):
    page.goto(f"{BASE_URL}/automation-practice-form", wait_until="domcontentloaded")
    page.wait_for_timeout(2000)

    # Remove ads/overlays
    page.evaluate(
        "document.querySelectorAll('ins.adsbygoogle, iframe[src*=google], "
        "iframe[src*=doubleclick], #fixedban, footer').forEach(e => e.remove())"
    )

    # Type into the Subjects autocomplete input
    subjects_input = page.locator("#subjectsInput")
    subjects_input.click()
    subjects_input.type("Ma")
    page.wait_for_timeout(1000)

    # Click "Maths" from the dropdown (Enter key would submit form — use click instead)
    page.locator(".subjects-auto-complete__option", has_text="Maths").first.click()

    # Maths tag should appear in the subjects container
    expect(
        page.locator(".subjects-auto-complete__multi-value__label", has_text="Maths")
    ).to_be_visible(timeout=5000)

    # Dropdown should be closed
    expect(page.locator(".subjects-auto-complete__menu")).to_be_hidden(timeout=3000)
