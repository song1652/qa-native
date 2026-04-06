"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_10_js_prompt_input (tc_10)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
import json
from pathlib import Path

from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_js_prompt_input(page):
    """JS Prompt 입력"""
    with open(TEST_DATA_PATH) as f:
        test_data = json.load(f)
    prompt_text = test_data["heroku"]["js_prompt"]["text"]

    page.goto(BASE_URL + "javascript_alerts")

    # Set up dialog handler to fill text and accept
    page.on("dialog", lambda dialog: dialog.accept(prompt_text))

    page.locator("button", has_text="Click for JS Prompt").click()

    expect(page.locator("#result")).to_contain_text(
        f"You entered: {prompt_text}", timeout=10000
    )
