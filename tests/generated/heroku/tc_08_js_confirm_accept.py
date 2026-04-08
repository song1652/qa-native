"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_08_js_confirm_accept (tc_08)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_tc_08_js_confirm_accept(page):
    """JS Confirm 버튼 클릭 후 OK 수락, 결과 텍스트에 Ok 표시 확인"""
    page.goto(BASE_URL + "javascript_alerts")
    page.wait_for_load_state("domcontentloaded")
    page.on("dialog", lambda d: d.accept())
    page.locator("button[onclick='jsConfirm()']").click()
    expect(page.locator("#result")).to_contain_text("You clicked: Ok", timeout=10000)
