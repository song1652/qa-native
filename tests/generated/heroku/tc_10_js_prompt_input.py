"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: test_js_prompt_input (tc_10)

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
    """JS Prompt 입력 — Prompt에 텍스트 입력 후 결과 확인"""
    with open(TEST_DATA_PATH, encoding="utf-8") as f:
        data = json.load(f)["heroku"]["js_prompt"]

    page.goto(BASE_URL + "javascript_alerts")

    page.on("dialog", lambda dialog: dialog.accept(prompt_text=data["text"]))

    page.locator("button", has_text="Click for JS Prompt").click()

    expect(page.locator("#result")).to_contain_text(
        f"You entered: {data['text']}", timeout=5000
    )
