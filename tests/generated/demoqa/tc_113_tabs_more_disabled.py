from pathlib import Path
from playwright.sync_api import Page, expect

BASE_URL = "https://demoqa.com"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"


def test_tabs_more_tab_disabled(page: Page) -> None:
    """tc_113: Tabs More Tab Disabled — verify 'More' tab is disabled and cannot be activated."""
    page.goto(f"{BASE_URL}/tabs", wait_until="domcontentloaded")
    page.wait_for_timeout(2000)

    # Remove ads/overlays
    page.evaluate(
        "document.querySelectorAll('ins.adsbygoogle, iframe[src*=google], iframe[src*=doubleclick]')"
        ".forEach(e => e.remove())"
    )

    # Find "More" tab
    more_tab = page.get_by_role("tab", name="More")
    expect(more_tab).to_be_visible(timeout=10000)

    # Verify the "More" tab is disabled
    # Bootstrap tabs use aria-disabled="true" or the tab element has class "disabled"
    aria_disabled = more_tab.get_attribute("aria-disabled")
    tab_class = more_tab.get_attribute("class") or ""

    assert aria_disabled == "true" or "disabled" in tab_class, (
        f"'More' tab should be disabled. aria-disabled={aria_disabled!r}, class={tab_class!r}"
    )

    # Record which tab is active before clicking
    active_tab_before = page.locator(".nav-tabs .nav-link.active").inner_text()

    # Attempt to click the "More" tab
    more_tab.click(force=True)
    page.wait_for_timeout(300)

    # Verify the active tab has NOT changed (More tab click had no effect)
    active_tab_after = page.locator(".nav-tabs .nav-link.active").inner_text()
    assert active_tab_before == active_tab_after, (
        f"Active tab changed after clicking disabled 'More' tab: "
        f"before={active_tab_before!r}, after={active_tab_after!r}"
    )
