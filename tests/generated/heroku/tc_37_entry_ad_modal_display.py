from pathlib import Path
from playwright.sync_api import Page, expect

BASE_URL = "https://the-internet.herokuapp.com/"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"


def test_entry_ad_modal_display(page: Page):
    """Entry Ad 모달 표시 확인"""
    page.goto(f"{BASE_URL}entry_ad")
    page.wait_for_load_state("domcontentloaded")

    # 모달 다이얼로그 표시 대기
    modal = page.locator("#modal")
    expect(modal).to_be_visible(timeout=10000)

    # 모달 제목 텍스트 확인
    modal_title = page.locator("#modal h3")
    expect(modal_title).to_contain_text("This is a modal window", timeout=5000)
