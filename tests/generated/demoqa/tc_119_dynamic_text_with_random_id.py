from pathlib import Path
from playwright.sync_api import Page, expect

BASE_URL = "https://demoqa.com"
TEST_DATA_PATH = (
    Path(__file__).resolve().parent.parent.parent.parent
    / "config" / "test_data.json"
)


def test_dynamic_text_with_random_id(page: Page):
    page.goto(f"{BASE_URL}/dynamic-properties")
    page.wait_for_load_state("domcontentloaded")
    page.wait_for_timeout(2000)

    # Remove ads/overlays
    page.evaluate(
        "document.querySelectorAll("
        "'ins.adsbygoogle, iframe[src*=google],"
        " iframe[src*=doubleclick], #fixedban, footer'"
        ").forEach(e => e.remove())"
    )

    # Find the element with "This text has random Id"
    random_id_elem = page.locator("p").filter(
        has_text="This text has random Id"
    )
    expect(random_id_elem).to_be_visible(timeout=5000)

    # Verify the element has a non-empty id attribute
    element_id = random_id_elem.get_attribute("id")
    assert element_id is not None and element_id.strip() != "", (
        f"Expected non-empty id, got: {element_id!r}"
    )
