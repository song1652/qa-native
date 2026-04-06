from pathlib import Path
from playwright.sync_api import Page, expect

BASE_URL = "https://demoqa.com"
TEST_DATA_PATH = (
    Path(__file__).resolve().parent.parent.parent.parent
    / "config" / "test_data.json"
)


def test_form_subject_remove_tag(page: Page):
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

    # Type into subjects input to trigger autocomplete
    subjects_input = page.locator("#subjectsInput")
    subjects_input.click()
    subjects_input.type("Maths")
    page.wait_for_timeout(1000)

    # Click autocomplete option (Enter submits form)
    option = (
        page.locator(".subjects-auto-complete__option")
        .filter(has_text="Maths")
        .first
    )
    expect(option).to_be_visible(timeout=5000)
    option.click()
    page.wait_for_timeout(500)

    # Verify the tag was added
    tag = (
        page.locator(".subjects-auto-complete__multi-value__label")
        .filter(has_text="Maths")
    )
    expect(tag).to_be_visible(timeout=5000)

    # Click the X button to remove the tag
    remove_btn = (
        page.locator(".subjects-auto-complete__multi-value__remove").first
    )
    expect(remove_btn).to_be_visible(timeout=5000)
    remove_btn.click()
    page.wait_for_timeout(500)

    # Verify the tag is removed
    labels = page.locator(".subjects-auto-complete__multi-value__label")
    expect(labels).to_have_count(0)
