"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/key_presses
케이스: tc_106_enter_key_detection (tc_106)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com"


def test_tc_106_enter_key_detection(page):
    """Enter 키 입력 감지"""
    page.goto(f"{BASE_URL}/key_presses")
    page.wait_for_load_state("networkidle")

    # Enter triggers form submit → page reload → #result text disappears.
    # Prevent form submission before pressing Enter.
    page.evaluate("""
        document.querySelector('form').addEventListener('submit', function(e) {
            e.preventDefault();
        });
    """)

    page.locator("#target").click()
    page.keyboard.press("Enter")

    result = page.locator("#result")
    expect(result).to_contain_text("You entered: ENTER", timeout=5000)
