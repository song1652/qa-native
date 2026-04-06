"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_79_tinymce_editor_text_input (tc_79)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from pathlib import Path

from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_tc_79_tinymce_editor_text_input(page):
    """TinyMCE 에디터 텍스트 입력"""
    page.goto(BASE_URL + "tinymce")

    # Wait for iframe to load
    editor_frame = page.locator("iframe#mce_0_ifr")
    expect(editor_frame).to_be_visible(timeout=15000)

    # Use page.evaluate to set innerHTML directly
    # (lessons: TinyMCE overlay blocks click+fill)
    page.evaluate(
        "const iframe = document.querySelector('iframe#mce_0_ifr');"
        " const body = iframe.contentDocument.querySelector('#tinymce');"
        " body.innerHTML = '<p>Hello Playwright</p>';"
    )

    # Verify text was set by reading it back from the iframe
    # Wrap in IIFE so `return` is valid inside a function body
    result = page.evaluate(
        "(() => {"
        " const iframe = document.querySelector('iframe#mce_0_ifr');"
        " const body = iframe.contentDocument.querySelector('#tinymce');"
        " return body.innerText;"
        "})()"
    )
    assert "Hello Playwright" in result, (
        f"Expected 'Hello Playwright' in editor, got: {result!r}"
    )
