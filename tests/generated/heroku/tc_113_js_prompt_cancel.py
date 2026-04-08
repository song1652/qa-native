"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_113_js_prompt_cancel (tc_113)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_tc_113_js_prompt_cancel(page):
    """JS Prompt Cancel 클릭 후 결과에 You entered: null 확인"""
    page.goto(BASE_URL + "javascript_alerts")
    page.wait_for_load_state("domcontentloaded")
    page.on("dialog", lambda d: d.dismiss())
    page.locator("button[onclick='jsPrompt()']").click()
    expect(page.locator("#result")).to_contain_text("You entered: null", timeout=10000)
