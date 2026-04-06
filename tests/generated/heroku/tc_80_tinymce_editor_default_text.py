from pathlib import Path
from playwright.sync_api import Page, expect

BASE_URL = "https://the-internet.herokuapp.com/"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"


def test_tinymce_editor_default_text(page: Page):
    page.goto("https://the-internet.herokuapp.com/tinymce")
    page.wait_for_load_state("domcontentloaded")
    page.wait_for_timeout(2000)

    tinymce_frame = page.frame_locator("iframe#mce_0_ifr")
    expect(tinymce_frame.locator("body#tinymce")).to_be_visible(timeout=15000)

    content = page.evaluate("""() => {
        const iframe = document.querySelector('iframe#mce_0_ifr');
        if (iframe && iframe.contentDocument) {
            const body = iframe.contentDocument.querySelector('#tinymce');
            return body ? body.innerText : '';
        }
        return '';
    }""")

    assert "Your content goes here." in content, f"Expected default text in editor, got: {content}"
