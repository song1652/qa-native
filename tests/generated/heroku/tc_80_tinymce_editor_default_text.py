"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_80_tinymce_editor_default_text (tc_80)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from pathlib import Path

BASE_URL = "https://the-internet.herokuapp.com/"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_tc_80_tinymce_editor_default_text(page):
    """TinyMCE 에디터 기본 텍스트 Your content goes here. 확인"""
    page.goto("https://the-internet.herokuapp.com/tinymce")
    page.wait_for_load_state("domcontentloaded")

    # Wait for TinyMCE editor iframe to load
    page.locator("iframe.tox-edit-area__iframe").wait_for(timeout=15000)

    # Read default content from iframe contentDocument
    content = page.evaluate(
        """() => {
            const iframe = document.querySelector('iframe.tox-edit-area__iframe');
            return iframe.contentDocument.querySelector('#tinymce').innerText;
        }"""
    )
    assert content is not None
    assert "Your content goes here." in content
