"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_107_escape_key_detection (tc_107)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_tc_107_escape_key_detection(page):
    """입력 영역에서 Escape 키 입력 후 You entered: ESCAPE 확인"""
    page.goto(BASE_URL + "key_presses")
    page.wait_for_load_state("domcontentloaded")
    page.locator("#target").click()
    page.keyboard.press("Escape")
    expect(page.locator("#result")).to_contain_text("You entered: ESCAPE", timeout=5000)
