from pathlib import Path
from playwright.sync_api import Page, expect

BASE_URL = "https://the-internet.herokuapp.com/"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"


def test_dynamic_controls_input_disabled_state(page: Page):
    # Dynamic Controls: 비활성화 상태에서 입력 필드 disabled 속성 확인
    page.goto("https://the-internet.herokuapp.com/dynamic_controls")
    page.wait_for_load_state("domcontentloaded")

    # 입력 필드가 disabled 속성을 가지는지 확인
    input_field = page.locator("#input-example input[type=text]")
    expect(input_field).to_be_disabled(timeout=5000)

    # disabled 상태에서 입력 불가 - is_disabled() 값 확인
    assert input_field.is_disabled(), "Input field should be disabled"
