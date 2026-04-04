"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: test_dynamic_controls_checkbox_remove_add (tc_12)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"


def test_dynamic_controls_checkbox_remove_add(page):
    """Dynamic Controls 체크박스 제거/추가 — Remove->gone, Add->back 확인"""
    page.goto(BASE_URL + "dynamic_controls")

    # lessons_learned: #message 텍스트 출현으로 대기 (중복 #loading 회피)
    checkbox = page.locator("#checkbox-example input[type='checkbox']")
    message = page.locator("#message")

    # Remove
    page.locator("button", has_text="Remove").click()
    expect(message).to_contain_text("It's gone!", timeout=10000)
    expect(checkbox).to_have_count(0, timeout=5000)

    # Add
    page.locator("button", has_text="Add").click()
    expect(message).to_contain_text("It's back!", timeout=10000)
    expect(page.locator("#checkbox-example input[type='checkbox']")).to_have_count(1, timeout=5000)
