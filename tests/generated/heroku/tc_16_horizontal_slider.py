"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/horizontal_slider
케이스: test_horizontal_slider (tc_16)
"""
BASE_URL = "https://the-internet.herokuapp.com"


def test_horizontal_slider(page):
    """슬라이더 값 조작 — ArrowRight 5회"""
    page.goto(f"{BASE_URL}/horizontal_slider")

    slider = page.locator("input[type=range]")
    slider.click()

    for _ in range(5):
        slider.press("ArrowRight")

    value = page.locator("#range").inner_text()
    assert float(value) > 0, f"슬라이더 값이 0보다 커야 함, 실제: {value}"
