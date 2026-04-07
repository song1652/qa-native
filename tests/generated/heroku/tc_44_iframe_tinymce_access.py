"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_44_iframe_tinymce_access (tc_44)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_tc_44_iframe_tinymce_access(page):
    """iFrame 링크 클릭 후 TinyMCE 에디터 iframe 존재 확인"""
    page.goto("https://the-internet.herokuapp.com/iframe")
    page.wait_for_load_state("domcontentloaded")

    # Wait for TinyMCE editor iframe — TinyMCE 6+ uses tox-edit-area__iframe
    editor_iframe = page.locator("iframe.tox-edit-area__iframe")
    expect(editor_iframe).to_be_visible(timeout=15000)

    # Access editor content via page.evaluate and set innerHTML
    frame = page.frame_locator("iframe.tox-edit-area__iframe")
    body = frame.locator("#tinymce")
    expect(body).to_be_visible(timeout=10000)

    # Set content via evaluate to avoid toolbar overlay interference
    page.evaluate(
        """() => {
            const iframe = document.querySelector('iframe.tox-edit-area__iframe');
            if (iframe && iframe.contentDocument) {
                const body = iframe.contentDocument.querySelector('#tinymce');
                if (body) body.innerHTML = '<p>Test content</p>';
            }
        }"""
    )

    content = page.evaluate(
        """() => {
            const iframe = document.querySelector('iframe.tox-edit-area__iframe');
            if (iframe && iframe.contentDocument) {
                const body = iframe.contentDocument.querySelector('#tinymce');
                return body ? body.innerHTML : '';
            }
            return '';
        }"""
    )
    assert "Test content" in content
