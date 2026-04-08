"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_91_dropdown_default_value (tc_91)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"


def test_tc_91_dropdown_default_value(page):
    """드롭다운 기본 선택값 Please select an option 및 disabled 상태 확인"""
    page.goto("https://the-internet.herokuapp.com/dropdown")
    page.wait_for_load_state("domcontentloaded")

    dropdown = page.locator("#dropdown")
    expect(dropdown).to_be_visible()

    # <option> 요소는 Playwright에서 hidden 처리되므로 JS로 selectedIndex 텍스트 검증
    selected_text = page.evaluate(
        "() => { const sel = document.getElementById('dropdown'); return sel.options[sel.selectedIndex].text; }"
    )
    assert selected_text == "Please select an option", (
        f"Expected default 'Please select an option', got '{selected_text}'"
    )

    # disabled 속성 확인
    disabled_option_count = page.evaluate(
        "() => document.querySelectorAll('#dropdown option[disabled]').length"
    )
    assert disabled_option_count > 0, "Expected a disabled option but none found"
