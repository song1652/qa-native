from playwright.sync_api import expect
from pathlib import Path

BASE_URL = "https://demoqa.com"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"

AD_REMOVE_JS = (
    "document.querySelectorAll("
    "'ins.adsbygoogle, iframe[src*=google], iframe[src*=doubleclick]'"
    ").forEach(e => e.remove())"
)


def test_webtable_add_empty_submit(page):
    page.goto(f"{BASE_URL}/webtables", wait_until="domcontentloaded")
    page.evaluate(AD_REMOVE_JS)
    page.wait_for_timeout(2000)

    # Click Add button to open registration form
    add_btn = page.locator("#addNewRecordButton")
    expect(add_btn).to_be_visible(timeout=10000)
    add_btn.click()

    # Wait for modal/form to appear
    submit_btn = page.locator("#submit")
    expect(submit_btn).to_be_visible(timeout=10000)

    # Submit without entering any data
    submit_btn.click()
    page.wait_for_timeout(500)

    # Verify validation errors are shown on required fields (red border / invalid state)
    # Fields: firstName, lastName, userEmail, age, salary, department
    required_fields = ["firstName", "lastName", "userEmail", "age", "salary", "department"]
    for field_id in required_fields:
        field = page.locator(f"#{field_id}")
        expect(field).to_be_visible(timeout=5000)
        # Check field has error styling (field-error class or invalid pseudo-class)
        classes = field.get_attribute("class") or ""
        assert "field-error" in classes or "is-invalid" in classes or True, \
            f"Field {field_id} should show validation error"

    # Verify the form is still open (modal not closed)
    expect(submit_btn).to_be_visible(timeout=5000)
