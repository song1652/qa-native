from playwright.sync_api import expect
from pathlib import Path

BASE_URL = "https://demoqa.com"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"


def test_textbox_empty_submit(page):
    page.goto(f"{BASE_URL}/text-box", wait_until="domcontentloaded")
    page.wait_for_timeout(2000)

    # Remove ads
    page.evaluate(
        "document.querySelectorAll('ins.adsbygoogle, iframe[src*=google],"
        " iframe[src*=doubleclick]').forEach(e => e.remove())"
    )

    page.locator("#submit").click()
    page.wait_for_timeout(1000)

    output = page.locator("#output")
    # Output should not be visible or should be empty when nothing is submitted
    is_visible = output.is_visible()
    if is_visible:
        expect(output).not_to_contain_text("Name:")
        expect(output).not_to_contain_text("Email:")
