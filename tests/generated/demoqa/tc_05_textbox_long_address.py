from playwright.sync_api import expect
from pathlib import Path

BASE_URL = "https://demoqa.com"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"


def test_textbox_long_address(page):
    page.goto(f"{BASE_URL}/text-box", wait_until="domcontentloaded")
    page.wait_for_timeout(2000)

    # Remove ads
    page.evaluate(
        "document.querySelectorAll('ins.adsbygoogle, iframe[src*=google],"
        " iframe[src*=doubleclick]').forEach(e => e.remove())"
    )

    long_address = "A" * 300

    page.locator("#currentAddress").fill(long_address)
    page.locator("#submit").click()

    output = page.locator("#output")
    expect(output).to_be_visible(timeout=10000)

    # Verify the full address is displayed without truncation
    output_text = output.inner_text()
    assert long_address in output_text, (
        f"Expected full 300-char address in output, but it was truncated. "
        f"Output length: {len(output_text)}"
    )
