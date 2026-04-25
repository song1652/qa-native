"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_07_js_prompt_input (tc_07)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
import json
from pathlib import Path

BASE_URL = "https://the-internet.herokuapp.com/"
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_tc_07_js_prompt_input(page):
    """JS Prompt에 test_data 텍스트 입력 후 accept → #result에 입력 텍스트가 포함된 메시지 표시"""
    td = json.loads(TEST_DATA_PATH.read_text(encoding="utf-8"))
    prompt_text = td["heroku"]["js_prompt"]["text"]

    page.goto("https://the-internet.herokuapp.com/javascript_alerts")

    # Playwright sync API auto-dismisses prompt dialogs before async handlers run.
    # Override window.prompt directly so the button click returns the desired text.
    page.evaluate(f"window.prompt = () => {repr(prompt_text)};")
    page.locator("button", has_text="Click for JS Prompt").click()
    page.wait_for_timeout(500)

    result = page.locator("#result")
    result.wait_for(state="visible", timeout=5000)
    assert f"You entered: {prompt_text}" in result.inner_text()
