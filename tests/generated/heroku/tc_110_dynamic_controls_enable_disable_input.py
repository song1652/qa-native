from pathlib import Path
from playwright.sync_api import Page, expect

BASE_URL = "https://the-internet.herokuapp.com/"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"


def test_dynamic_controls_enable_disable_input(page: Page):
    # Dynamic Controls: 입력 필드 활성화 후 비활성화 확인
    page.goto("https://the-internet.herokuapp.com/dynamic_controls")
    page.wait_for_load_state("domcontentloaded")

    # 입력 필드가 초기에 비활성화 상태인지 확인
    input_field = page.locator("#input-example input[type=text]")
    expect(input_field).to_be_disabled(timeout=5000)

    # Enable 버튼 클릭
    page.locator("#input-example button").click()

    # 입력 필드 활성화 대기 (#message 텍스트 출현으로 대기)
    expect(page.locator("#message")).to_be_visible(timeout=10000)
    expect(input_field).to_be_enabled(timeout=5000)

    # Disable 버튼 클릭
    page.locator("#input-example button").click()

    # 입력 필드 비활성화 대기
    expect(page.locator("#message")).to_be_visible(timeout=10000)
    expect(input_field).to_be_disabled(timeout=5000)
