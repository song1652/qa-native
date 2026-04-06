"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_80_tinymce_editor_default_text (tc_80)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from pathlib import Path

from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_tc_80_tinymce_editor_default_text(page):
    """TinyMCE 에디터 기본 텍스트 읽기"""
    page.goto(BASE_URL + "tinymce")

    # Wait for iframe to load
    editor_frame = page.locator("iframe#mce_0_ifr")
    expect(editor_frame).to_be_visible(timeout=15000)

    # Read default text from iframe body#tinymce using innerText
    # Wrap in IIFE so `return` is valid inside a function body
    default_text = page.evaluate(
        "(() => {"
        " const iframe = document.querySelector('iframe#mce_0_ifr');"
        " const body = iframe.contentDocument.querySelector('#tinymce');"
        " return body.innerText;"
        "})()"
    )

    # lessons_learned: "Your content goes here." is the known default text
    assert "Your content goes here." in default_text, (
        f"Expected default text not found. Got: {default_text!r}"
    )
