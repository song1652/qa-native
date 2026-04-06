from pathlib import Path
from playwright.sync_api import Page, expect

BASE_URL = "https://the-internet.herokuapp.com/"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"


def test_dynamic_controls_add_remove(page: Page):
    """TC-12: Dynamic Controls 체크박스 제거/추가"""
    page.goto("https://the-internet.herokuapp.com/dynamic_controls")
    page.wait_for_load_state("domcontentloaded")

    # Remove 버튼 클릭
    remove_btn = page.get_by_role("button", name="Remove")
    expect(remove_btn).to_be_visible(timeout=10000)
    remove_btn.click()

    # "It's gone!" 메시지 대기 (중복 #loading 문제로 #message 텍스트로 대기)
    message = page.locator("#message")
    expect(message).to_contain_text("It's gone!", timeout=15000)

    # 체크박스가 사라졌는지 확인 - lessons_learned: 재추가 후에는 #checkbox-example input[type=checkbox] 사용
    checkbox = page.locator("#checkbox-example input[type=checkbox]")
    expect(checkbox).to_be_hidden(timeout=5000)

    # Add 버튼 클릭
    add_btn = page.get_by_role("button", name="Add")
    expect(add_btn).to_be_visible(timeout=5000)
    add_btn.click()

    # "It's back!" 메시지 대기
    expect(message).to_contain_text("It's back!", timeout=15000)

    # 체크박스가 다시 나타났는지 확인
    expect(checkbox).to_be_visible(timeout=5000)
