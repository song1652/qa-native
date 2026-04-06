"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_120_number_input_negative (tc_120)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"


def test_tc_120_number_input_negative(page):
    """숫자 입력 필드에 음수 입력"""
    page.goto(BASE_URL + "inputs")

    number_input = page.locator("input[type='number']")
    expect(number_input).to_be_visible(timeout=5000)

    number_input.click()
    number_input.fill("-5")

    # verify the value was accepted
    value = number_input.input_value()
    assert value == "-5", f"Expected '-5' but got '{value}'"
