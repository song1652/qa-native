"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_37_entry_ad_modal_display (tc_37)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"


def test_entry_ad_modal_display(page):
    """Entry Ad 모달 표시 확인"""
    page.goto(BASE_URL + "entry_ad")

    # 모달이 표시될 때까지 대기 - id="modal"
    modal = page.locator("#modal")
    expect(modal).to_be_visible(timeout=10000)

    # 모달 제목 텍스트 확인
    modal_title = page.locator("#modal .modal-title")
    expect(modal_title).to_contain_text(
        "This is a modal window", timeout=10000
    )
