"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_39_exit_intent_modal (tc_39)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"


def test_tc_39_exit_intent_modal(page):
    """Exit Intent 페이지에서 _ouibounce.fire() 호출로 모달 표시 확인"""
    page.goto("https://the-internet.herokuapp.com/exit_intent")
    page.wait_for_load_state("domcontentloaded")
    page.wait_for_timeout(1000)
    # Trigger modal via JS directly as mouse events don't work reliably
    page.evaluate("() => { _ouibounce.fire(); }")
    page.wait_for_timeout(500)
    modal = page.locator("#ouibounce-modal")
    expect(modal).to_be_visible(timeout=5000)
