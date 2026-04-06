"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_118_horizontal_slider_min (tc_118)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"


def test_tc_118_horizontal_slider_min(page):
    """수평 슬라이더 최소값 설정"""
    page.goto(BASE_URL + "horizontal_slider")

    slider = page.locator("input[type='range']")
    expect(slider).to_be_visible(timeout=5000)

    # press Home key to jump to minimum value
    slider.click()
    slider.press("Home")

    expect(page.locator("#range")).to_have_text("0", timeout=5000)
