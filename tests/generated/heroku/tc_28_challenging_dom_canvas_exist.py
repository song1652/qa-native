"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_28_challenging_dom_canvas_exist (tc_28)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_tc_28_challenging_dom_canvas_exist(page):
    """Challenging DOM Canvas 존재 확인"""
    page.goto(BASE_URL + "challenging_dom")
    expect(page.locator("body")).to_be_visible()

    canvas = page.locator("canvas#canvas")
    expect(canvas).to_be_visible(timeout=10000)

    canvas_id = canvas.get_attribute("id")
    assert canvas_id == "canvas", f"Expected id='canvas', got: {canvas_id}"
