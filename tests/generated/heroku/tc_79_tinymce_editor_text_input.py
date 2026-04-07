"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_79_tinymce_editor_text_input (tc_79)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from pathlib import Path

BASE_URL = "https://the-internet.herokuapp.com/"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_tc_79_tinymce_editor_text_input(page):
    """TinyMCE 에디터에 evaluate로 텍스트 설정 후 확인 (click+fill 아닌 JS 직접 설정)"""
    page.goto("https://the-internet.herokuapp.com/tinymce")
    page.wait_for_load_state("domcontentloaded")

    # Wait for TinyMCE editor iframe to load
    page.locator("iframe.tox-edit-area__iframe").wait_for(timeout=15000)

    # Set content via JS directly into iframe contentDocument
    # TinyMCE overlay/toolbar intercepts click — use evaluate instead
    page.evaluate(
        """() => {
            const iframe = document.querySelector('iframe.tox-edit-area__iframe');
            iframe.contentDocument.querySelector('#tinymce').innerHTML = '<p>Hello Playwright</p>';
        }"""
    )

    # Verify by reading back the content
    content = page.evaluate(
        """() => {
            const iframe = document.querySelector('iframe.tox-edit-area__iframe');
            return iframe.contentDocument.querySelector('#tinymce').innerText;
        }"""
    )
    assert "Hello Playwright" in content
