from playwright.sync_api import expect
from pathlib import Path

BASE_URL = "https://demoqa.com"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"


def test_textbox_only_name(page):
    page.goto(f"{BASE_URL}/text-box", wait_until="domcontentloaded")
    page.wait_for_timeout(2000)

    # Remove ads
    page.evaluate(
        "document.querySelectorAll('ins.adsbygoogle, iframe[src*=google],"
        " iframe[src*=doubleclick]').forEach(e => e.remove())"
    )

    page.locator("#userName").fill("Jane Smith")
    page.locator("#submit").click()

    output = page.locator("#output")
    expect(output).to_be_visible(timeout=10000)
    expect(output).to_contain_text("Jane Smith")

    # Email, Current Address, Permanent Address should not appear in output
    expect(output).not_to_contain_text("Email:")
    expect(output).not_to_contain_text("Current Address:")
    expect(output).not_to_contain_text("Permanent Address:")
