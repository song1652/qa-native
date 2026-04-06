"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_16_slider_value_manipulation (tc_16)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_tc_16_slider_value_manipulation(page):
    """슬라이더 값 조작"""
    page.goto(BASE_URL + "horizontal_slider")
    expect(page.locator("body")).to_be_visible()

    slider = page.locator("input[type='range']")
    expect(slider).to_be_visible()

    # Click to focus, then press ArrowRight 5 times
    slider.click()
    for _ in range(5):
        slider.press("ArrowRight")

    page.wait_for_timeout(300)

    range_value = page.locator("#range").inner_text()
    assert float(range_value) > 0, f"Expected value > 0, got: {range_value}"
