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


def test_tc_10_js_prompt_input(page):
    """JS Prompt에 텍스트 입력 후 OK, 결과 텍스트 확인"""
    data = json.load(open(TEST_DATA_PATH))["heroku"]["js_prompt"]
    prompt_text = data["text"]
    page.goto(BASE_URL + "javascript_alerts")
    page.wait_for_load_state("domcontentloaded")
    page.on("dialog", lambda d: d.accept(prompt_text))
    page.locator("button[onclick='jsPrompt()']").click()
    expect(page.locator("#result")).to_contain_text(f"You entered: {prompt_text}", timeout=10000)
