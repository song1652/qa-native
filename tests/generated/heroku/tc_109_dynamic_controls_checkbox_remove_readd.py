"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/dynamic_controls
케이스: tc_109_dynamic_controls_checkbox_remove_readd (tc_109)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com"


def test_tc_109_dynamic_controls_checkbox_remove_readd(page):
    """Dynamic Controls 체크박스 제거 후 재추가"""
    page.goto(f"{BASE_URL}/dynamic_controls")
    page.wait_for_load_state("networkidle")

    # Verify checkbox is initially present
    expect(page.locator("#checkbox-example input[type=checkbox]")).to_be_visible()

    # Click Remove button
    page.locator("#checkbox-example button").click()

    # Wait for "It's gone!" message — avoids #loading ambiguity
    expect(page.locator("#message")).to_contain_text("It's gone!", timeout=10000)

    # Checkbox should now be gone
    expect(page.locator("#checkbox-example input[type=checkbox]")).not_to_be_visible()

    # Click Add button
    page.locator("#checkbox-example button").click()

    # Wait for "It's back!" message
    expect(page.locator("#message")).to_contain_text("It's back!", timeout=10000)

    # After re-add, #checkbox becomes input itself — use scoped selector
    expect(page.locator("#checkbox-example input[type=checkbox]")).to_be_visible()
