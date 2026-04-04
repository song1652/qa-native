"""Playwright 테스트 — test_horizontal_slider (tc_16)"""

BASE_URL = "https://the-internet.herokuapp.com/"


def test_horizontal_slider(page):
    page.goto(BASE_URL + "horizontal_slider")
    slider = page.locator("input[type='range']")
    slider.click()
    for _ in range(5):
        slider.press("ArrowRight")
    range_value = page.locator("#range")
    value_text = range_value.inner_text()
    assert float(value_text) > 0, f"Expected slider value > 0, got {value_text}"
