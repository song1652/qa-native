"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: test_dynamic_controls_input_enable (tc_13)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"


def test_dynamic_controls_input_enable(page):
    """Dynamic Controls 입력 필드 활성화 — disabled 확인 후 Enable 클릭"""
    page.goto(BASE_URL + "dynamic_controls")

    # lessons_learned: #message 텍스트 대기 (중복 #loading 회피)
    text_input = page.locator("#input-example input[type='text']")
    message = page.locator("#message")

    expect(text_input).to_be_disabled(timeout=5000)

    page.locator("#input-example button", has_text="Enable").click()
    expect(message).to_contain_text("It's enabled!", timeout=10000)
    expect(text_input).to_be_enabled(timeout=5000)
