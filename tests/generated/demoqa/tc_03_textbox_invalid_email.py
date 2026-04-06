from playwright.sync_api import expect
from pathlib import Path

BASE_URL = "https://demoqa.com"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"


def test_textbox_invalid_email(page):
    page.goto(f"{BASE_URL}/text-box", wait_until="domcontentloaded")
    page.wait_for_timeout(2000)

    # Remove ads
    page.evaluate(
        "document.querySelectorAll('ins.adsbygoogle, iframe[src*=google],"
        " iframe[src*=doubleclick]').forEach(e => e.remove())"
    )

    page.locator("#userEmail").fill("invalid-email")
    page.locator("#submit").click()
    page.wait_for_timeout(1000)

    # Email field should show error class (red border) when invalid email submitted
    email_field = page.locator("#userEmail")
    expect(email_field).to_be_visible(timeout=5000)
    # Verify error styling is applied — demoqa adds 'field-error' class on invalid email
    classes = email_field.get_attribute("class") or ""
    assert "field-error" in classes or "error" in classes.lower(), (
        f"Expected error class on email field, got: {classes}"
    )
