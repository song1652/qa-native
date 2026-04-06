from pathlib import Path
from playwright.sync_api import Page, expect

BASE_URL = "https://the-internet.herokuapp.com/"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"


def test_exit_intent_modal_on_mouse_leave(page: Page):
    """Exit Intent 마우스 이탈 시 모달 표시"""
    page.goto(f"{BASE_URL}exit_intent")
    page.wait_for_load_state("domcontentloaded")
    page.wait_for_timeout(500)

    # 페이지 로드 확인
    expect(page.locator("body")).to_be_visible(timeout=5000)

    # _ouibounce.fire()로 모달 트리거 (aggressive:true, timer:0 설정)
    page.evaluate("() => { if(typeof _ouibounce !== 'undefined') _ouibounce.fire(); }")
    page.wait_for_timeout(500)

    # 모달 다이얼로그 표시 확인 (#ouibounce-modal)
    modal = page.locator("#ouibounce-modal")
    expect(modal).to_be_visible(timeout=5000)

    # 모달 제목 텍스트 확인
    modal_title = page.locator("#ouibounce-modal h3")
    expect(modal_title).to_contain_text("This is a modal window", timeout=5000)
