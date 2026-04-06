from pathlib import Path
from playwright.sync_api import Page, expect

BASE_URL = "https://the-internet.herokuapp.com/"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"


def test_tinymce_editor_text_input(page: Page):
    page.goto("https://the-internet.herokuapp.com/tinymce")
    page.wait_for_load_state("domcontentloaded")
    page.wait_for_timeout(2000)

    tinymce_frame = page.frame_locator("iframe#mce_0_ifr")
    expect(tinymce_frame.locator("body#tinymce")).to_be_visible(timeout=15000)

    page.evaluate("""() => {
        const iframe = document.querySelector('iframe#mce_0_ifr');
        if (iframe && iframe.contentDocument) {
            const body = iframe.contentDocument.querySelector('#tinymce');
            if (body) {
                body.innerHTML = '<p>Hello Playwright</p>';
            }
        }
    }""")

    page.wait_for_timeout(500)

    content = page.evaluate("""() => {
        const iframe = document.querySelector('iframe#mce_0_ifr');
        if (iframe && iframe.contentDocument) {
            const body = iframe.contentDocument.querySelector('#tinymce');
            return body ? body.innerText : '';
        }
        return '';
    }""")

    assert "Hello Playwright" in content, f"Expected 'Hello Playwright' in editor, got: {content}"
