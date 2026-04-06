from pathlib import Path
from playwright.sync_api import Page, expect

BASE_URL = "https://the-internet.herokuapp.com/"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"


def test_dynamic_controls_remove_and_add_checkbox(page: Page):
    # Dynamic Controls: 체크박스 제거 후 재추가 확인
    page.goto("https://the-internet.herokuapp.com/dynamic_controls")
    page.wait_for_load_state("domcontentloaded")

    # 체크박스 존재 확인 (초기 상태)
    checkbox = page.locator("#checkbox-example input[type=checkbox]")
    expect(checkbox).to_be_visible(timeout=5000)

    # Remove 버튼 클릭
    page.locator("#checkbox-example button").click()

    # 체크박스 사라짐 대기 (#message 텍스트 출현으로 대기 - #loading이 2개 존재 주의)
    expect(page.locator("#message")).to_be_visible(timeout=10000)
    expect(checkbox).to_be_hidden(timeout=5000)

    # Add 버튼 클릭
    page.locator("#checkbox-example button").click()

    # 체크박스 재표시 대기
    expect(page.locator("#message")).to_be_visible(timeout=10000)
    # 재추가 후 #checkbox-example input[type=checkbox] 셀렉터 사용
    expect(page.locator("#checkbox-example input[type=checkbox]")).to_be_visible(timeout=10000)
