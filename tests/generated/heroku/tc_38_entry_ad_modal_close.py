from pathlib import Path
from playwright.sync_api import Page, expect

BASE_URL = "https://the-internet.herokuapp.com/"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"


def test_entry_ad_modal_close(page: Page):
    """Entry Ad 모달 닫기"""
    page.goto(f"{BASE_URL}entry_ad")
    page.wait_for_load_state("domcontentloaded")

    # 모달 다이얼로그 표시 대기
    modal = page.locator("#modal")
    expect(modal).to_be_visible(timeout=10000)

    # 모달의 "Close" 버튼 클릭
    close_button = page.locator("#modal .modal-footer p")
    expect(close_button).to_be_visible(timeout=5000)
    close_button.click()

    # 모달이 사라졌는지 확인
    expect(modal).to_be_hidden(timeout=5000)

    # 페이지 본문 콘텐츠가 표시되는지 확인
    expect(page.locator("body")).to_be_visible(timeout=5000)
