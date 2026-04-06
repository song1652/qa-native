from pathlib import Path
from playwright.sync_api import Page, expect

BASE_URL = "https://the-internet.herokuapp.com/"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"


def test_tinymce_editor_load(page: Page):
    page.goto("https://the-internet.herokuapp.com/tinymce")
    page.wait_for_load_state("domcontentloaded")
    page.wait_for_timeout(2000)

    # TinyMCE 6+ uses tox-* class names; iframe class is tox-edit-area__iframe
    tinymce_frame = page.frame_locator("iframe.tox-edit-area__iframe")
    expect(tinymce_frame.locator("body")).to_be_visible(timeout=15000)

    # Editor header contains the toolbar/menubar
    toolbar = page.locator(".tox-editor-header, .mce-toolbar, .tox-toolbar")
    assert toolbar.count() > 0, "TinyMCE toolbar/editor-header should be present"
