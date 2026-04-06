"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/dynamic_controls
케이스: tc_111_dynamic_controls_disabled_input (tc_111)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com"


def test_tc_111_dynamic_controls_disabled_input(page):
    """Dynamic Controls 비활성화 상태에서 입력 시도"""
    page.goto(f"{BASE_URL}/dynamic_controls")
    page.wait_for_load_state("networkidle")

    text_input = page.locator("#input-example input[type=text]")

    # Verify input is disabled initially via attribute
    expect(text_input).to_be_disabled()

    disabled_attr = text_input.get_attribute("disabled")
    assert disabled_attr is not None, "Expected input to have disabled attribute"
