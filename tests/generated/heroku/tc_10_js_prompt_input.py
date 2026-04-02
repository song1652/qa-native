"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/javascript_alerts
케이스: test_js_prompt_input (tc_10)
"""
import json
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_js_prompt_input(page):
    """JS Prompt 입력 — 텍스트 입력 후 결과 검증"""
    data = json.loads(TEST_DATA_PATH.read_text(encoding="utf-8"))
    prompt_text = data["heroku"]["js_prompt"]["text"]

    page.goto(f"{BASE_URL}/javascript_alerts")

    page.on("dialog", lambda dialog: dialog.accept(prompt_text))
    page.locator("button", has_text="Click for JS Prompt").click()

    expect(page.locator("#result")).to_contain_text(
        f"You entered: {prompt_text}"
    )
