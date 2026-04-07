"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_119_horizontal_slider_max (tc_119)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_tc_119_horizontal_slider_max(page):
    """슬라이더를 최대값(5)으로 설정 후 표시 값 5 확인"""
    page.goto(BASE_URL + "horizontal_slider")
    page.wait_for_load_state("domcontentloaded")
    slider = page.locator("input[type='range']")
    slider.focus()
    # Press End key to go to maximum value
    page.keyboard.press("End")
    expect(page.locator("#range")).to_have_text("5", timeout=5000)
