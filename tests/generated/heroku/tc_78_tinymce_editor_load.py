"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_78_tinymce_editor_load (tc_78)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from pathlib import Path

from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_tc_78_tinymce_editor_load(page):
    """TinyMCE 에디터 로드 확인"""
    page.goto(BASE_URL + "tinymce")

    # Verify TinyMCE iframe exists and is visible
    editor_frame = page.locator("iframe#mce_0_ifr")
    expect(editor_frame).to_be_visible(timeout=15000)

    # Verify toolbar is present (tox-editor-header contains toolbar buttons)
    toolbar = page.locator(".tox-editor-header")
    expect(toolbar).to_be_visible(timeout=15000)
