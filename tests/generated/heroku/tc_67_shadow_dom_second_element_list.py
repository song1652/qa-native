from pathlib import Path
from playwright.sync_api import Page

BASE_URL = "https://the-internet.herokuapp.com/"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"


def test_shadow_dom_second_element_list(page: Page) -> None:
    page.goto("https://the-internet.herokuapp.com/shadowdom")
    page.wait_for_load_state("domcontentloaded")

    # lessons_learned: shadowRoot.textContent includes CSS style tag content.
    # The actual slot content lives in the light DOM (innerHTML of the host element).
    # Second my-paragraph has a <ul slot="my-text"> with list items including "In a list!"
    text = page.evaluate(
        "() => {"
        " const el = document.querySelectorAll('my-paragraph')[1];"
        " return el ? el.innerHTML : '';"
        " }"
    )

    assert text is not None and text != "", "Second shadow DOM host element not found"
    assert "In a list!" in text, f"Expected 'In a list!' in light DOM slot content, got: {text!r}"
