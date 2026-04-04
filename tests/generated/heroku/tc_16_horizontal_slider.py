"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: test_horizontal_slider (tc_16)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
BASE_URL = "https://the-internet.herokuapp.com/"


def test_horizontal_slider(page):
    """슬라이더 값 조작 — ArrowRight 5회 후 값 > 0 확인"""
    page.goto(BASE_URL + "horizontal_slider")

    slider = page.locator("input[type='range']")
    slider.click()

    for _ in range(5):
        slider.press("ArrowRight")

    range_value = page.locator("#range")
    value_text = range_value.inner_text()
    assert float(value_text) > 0, f"Expected slider value > 0, got {value_text}"
