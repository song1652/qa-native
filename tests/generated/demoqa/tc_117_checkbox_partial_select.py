import re
from pathlib import Path
from playwright.sync_api import Page, expect

BASE_URL = "https://demoqa.com"
TEST_DATA_PATH = (
    Path(__file__).resolve().parent.parent.parent.parent
    / "config" / "test_data.json"
)


def test_checkbox_partial_select_indeterminate_state(page: Page):
    page.goto(f"{BASE_URL}/checkbox")
    page.wait_for_load_state("domcontentloaded")
    page.wait_for_timeout(2000)

    # Remove ads/overlays
    page.evaluate(
        "document.querySelectorAll("
        "'ins.adsbygoogle, iframe[src*=google],"
        " iframe[src*=doubleclick], #fixedban, footer'"
        ").forEach(e => e.remove())"
    )

    # Expand Home node
    home_switcher = page.locator(".rc-tree-switcher_close").first
    expect(home_switcher).to_be_visible(timeout=5000)
    home_switcher.click()
    page.wait_for_timeout(500)

    # Expand Desktop node
    desktop_row = (
        page.locator(".rc-tree-treenode")
        .filter(has_text="Desktop")
        .first
    )
    desktop_switcher = desktop_row.locator(".rc-tree-switcher_close")
    expect(desktop_switcher).to_be_visible(timeout=5000)
    desktop_switcher.click()
    page.wait_for_timeout(500)

    # Check "Notes" checkbox
    notes_row = (
        page.locator(".rc-tree-treenode")
        .filter(has_text="Notes")
        .first
    )
    notes_cb = notes_row.locator(".rc-tree-checkbox").first
    expect(notes_cb).to_be_visible(timeout=5000)
    notes_cb.click()
    page.wait_for_timeout(500)

    # Verify Notes is checked
    expect(notes_cb).to_have_class(
        re.compile(r"rc-tree-checkbox-checked"), timeout=5000
    )

    # Verify Desktop is indeterminate
    desktop_cb = desktop_row.locator(".rc-tree-checkbox").first
    expect(desktop_cb).to_have_class(
        re.compile(r"rc-tree-checkbox-indeterminate"), timeout=5000
    )

    # Verify Home is indeterminate
    home_row = (
        page.locator(".rc-tree-treenode")
        .filter(has_text="Home")
        .first
    )
    home_cb = home_row.locator(".rc-tree-checkbox").first
    expect(home_cb).to_have_class(
        re.compile(r"rc-tree-checkbox-indeterminate"), timeout=5000
    )
