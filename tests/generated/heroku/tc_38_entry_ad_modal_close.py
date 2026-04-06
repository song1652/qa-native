"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_38_entry_ad_modal_close (tc_38)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"


def test_entry_ad_modal_close(page):
    """Entry Ad 모달 닫기"""
    page.goto(BASE_URL + "entry_ad")

    # 모달 표시 대기
    modal = page.locator("#modal")
    expect(modal).to_be_visible(timeout=10000)

    # 모달 footer의 Close 링크 클릭
    close_link = page.locator("#modal .modal-footer p")
    expect(close_link).to_be_visible(timeout=5000)
    close_link.click()

    # 모달이 사라졌는지 확인
    expect(modal).to_be_hidden(timeout=10000)

    # 페이지 본문 콘텐츠가 표시되는지 확인
    expect(page.locator("body")).to_be_visible()
