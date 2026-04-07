"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_28_challenging_dom_canvas (tc_28)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"


def test_tc_28_challenging_dom_canvas(page):
    """Challenging DOM 페이지에 canvas 요소 존재 및 id 속성 확인"""
    page.goto("https://the-internet.herokuapp.com/challenging_dom")
    canvas = page.locator("canvas")
    expect(canvas).to_be_visible(timeout=10000)
    canvas_id = canvas.get_attribute("id")
    assert canvas_id is not None and canvas_id != "", "canvas element should have an id attribute"
