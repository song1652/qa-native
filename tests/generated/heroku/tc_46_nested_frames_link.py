"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_46_nested_frames_link (tc_46)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_tc_46_nested_frames_link(page):
    """Nested Frames 링크 클릭 후 /nested_frames 이동 확인"""
    page.goto("https://the-internet.herokuapp.com/frames")
    page.wait_for_load_state("domcontentloaded")

    page.locator("a[href='/nested_frames']").click()
    page.wait_for_load_state("domcontentloaded")

    expect(page).to_have_url("https://the-internet.herokuapp.com/nested_frames", timeout=10000)
