import json
from pathlib import Path
from playwright.sync_api import Page, expect

BASE_URL = "https://demoqa.com"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"


def test_progress_bar_completes_to_100_and_shows_reset(page: Page):
    page.goto(f"{BASE_URL}/progress-bar", wait_until="domcontentloaded")
    page.wait_for_timeout(2000)
    page.evaluate(
        "document.querySelectorAll('ins.adsbygoogle, iframe[src*=google], iframe[src*=doubleclick], #fixedban, footer').forEach(e => e.remove())"
    )

    # Click Start button
    start_button = page.get_by_role("button", name="Start")
    expect(start_button).to_be_visible(timeout=10000)
    start_button.click()

    # Wait for progress bar to reach 100%
    progress_bar = page.locator("#progressBar .progress-bar")
    expect(progress_bar).to_be_visible(timeout=5000)

    # Poll until value reaches 100 (max 30 seconds)
    for _ in range(60):
        page.wait_for_timeout(500)
        aria_value = progress_bar.get_attribute("aria-valuenow")
        if aria_value and int(aria_value) >= 100:
            break

    aria_value = progress_bar.get_attribute("aria-valuenow")
    assert aria_value is not None, "aria-valuenow attribute not found"
    assert int(aria_value) == 100, f"Expected progress bar to reach 100%, got {aria_value}%"

    # Verify Reset button appears
    reset_button = page.get_by_role("button", name="Reset")
    expect(reset_button).to_be_visible(timeout=5000)
