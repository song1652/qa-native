"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: test_number_input (tc_20)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"


def test_number_input(page):
    """숫자 입력 필드 — 42 입력 후 값 및 type=number 확인"""
    page.goto(BASE_URL + "inputs")

    number_input = page.locator("input[type='number']")
    number_input.fill("42")

    expect(number_input).to_have_value("42", timeout=5000)
    expect(number_input).to_have_attribute("type", "number", timeout=5000)
