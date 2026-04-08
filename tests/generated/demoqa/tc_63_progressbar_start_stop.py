import json
from pathlib import Path
from playwright.sync_api import Page, expect

BASE_URL = "https://demoqa.com"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"


def test_progress_bar_starts_and_stops_at_intermediate_value(page: Page):
    page.goto(f"{BASE_URL}/progress-bar", wait_until="domcontentloaded")
    page.wait_for_timeout(2000)
    page.evaluate(
        "document.querySelectorAll('ins.adsbygoogle, iframe[src*=google], iframe[src*=doubleclick], #fixedban, footer').forEach(e => e.remove())"
    )

    # Click Start button
    start_button = page.get_by_role("button", name="Start")
    expect(start_button).to_be_visible(timeout=10000)
    start_button.click()

    # Wait a bit for the progress bar to advance
    page.wait_for_timeout(2000)

    # Click Stop button
    stop_button = page.get_by_role("button", name="Stop")
    expect(stop_button).to_be_visible(timeout=5000)
    stop_button.click()
    page.wait_for_timeout(500)

    # Verify progress bar stopped at a value between 0 and 100
    progress_bar = page.locator("#progressBar .progress-bar")
    expect(progress_bar).to_be_visible(timeout=5000)
    aria_value = progress_bar.get_attribute("aria-valuenow")
    assert aria_value is not None, "aria-valuenow attribute not found on progress bar"
    value = int(aria_value)
    assert 0 < value <= 100, f"Expected progress bar value to be between 1 and 100, got {value}"
