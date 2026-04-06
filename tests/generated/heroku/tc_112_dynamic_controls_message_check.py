from pathlib import Path
from playwright.sync_api import Page, expect

BASE_URL = "https://the-internet.herokuapp.com/"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"


def test_dynamic_controls_message_check(page: Page):
    # Dynamic Controls: Remove 후 "It's gone!" 메시지 확인
    page.goto("https://the-internet.herokuapp.com/dynamic_controls")
    page.wait_for_load_state("domcontentloaded")

    # Remove 버튼 클릭
    page.locator("#checkbox-example button").click()

    # 완료 메시지 대기 (#message 텍스트 출현으로 대기 - #loading 중복 문제 회피)
    message = page.locator("#message")
    expect(message).to_be_visible(timeout=10000)
    expect(message).to_contain_text("It's gone!", timeout=5000)
