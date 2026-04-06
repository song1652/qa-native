from pathlib import Path
from playwright.sync_api import Page

BASE_URL = "https://the-internet.herokuapp.com/"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"


def test_shadow_dom_first_element_text(page: Page) -> None:
    page.goto("https://the-internet.herokuapp.com/shadowdom")
    page.wait_for_load_state("domcontentloaded")

    text = page.evaluate(
        "() => {"
        " const el = document.querySelectorAll('my-paragraph')[0];"
        " return el && el.shadowRoot ? el.shadowRoot.textContent : '';"
        " }"
    )

    assert text is not None, "Shadow DOM host element not found"
    assert len(text.strip()) > 0, "Shadow DOM text is empty"
    assert "My default text" in text or "default" in text.lower(), (
        f"Expected default text in shadow DOM, got: {text!r}"
    )
