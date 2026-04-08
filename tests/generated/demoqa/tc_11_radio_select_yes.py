from pathlib import Path
from playwright.sync_api import Page, expect

BASE_URL = "https://demoqa.com"
TEST_DATA_PATH = (
    Path(__file__).resolve().parent.parent.parent.parent
    / "config" / "test_data.json"
)


def test_select_yes_radio_button(page: Page):
    page.goto(f"{BASE_URL}/radio-button")
    page.wait_for_load_state("domcontentloaded")
    page.wait_for_timeout(2000)

    # Remove ads/overlays
    page.evaluate(
        "document.querySelectorAll("
        "'ins.adsbygoogle, iframe[src*=google],"
        " iframe[src*=doubleclick], #fixedban, footer'"
        ").forEach(e => e.remove())"
    )

    # Click the "Yes" label (input is visually hidden)
    yes_label = page.locator("label[for='yesRadio']")
    expect(yes_label).to_be_visible(timeout=5000)
    yes_label.click()
    page.wait_for_timeout(500)

    # Verify radio is checked
    yes_radio = page.locator("#yesRadio")
    expect(yes_radio).to_be_checked(timeout=5000)

    # Verify confirmation text
    success_text = page.locator(".mt-3")
    expect(success_text).to_contain_text("Yes", timeout=5000)
