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
    """TinyMCE 에디터 iframe(iframe.tox-edit-area__iframe)과 툴바(.tox-editor-header) 존재 확인"""
    page.goto("https://the-internet.herokuapp.com/tinymce")
    page.wait_for_load_state("domcontentloaded")

    # TinyMCE 6+ uses iframe.tox-edit-area__iframe (not #mce_0_ifr)
    editor_iframe = page.locator("iframe.tox-edit-area__iframe")
    expect(editor_iframe).to_be_visible(timeout=15000)

    # Toolbar header
    toolbar = page.locator(".tox-editor-header")
    expect(toolbar).to_be_visible(timeout=10000)
