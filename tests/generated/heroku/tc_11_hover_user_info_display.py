"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_11_hover_user_info_display (tc_11)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_tc_11_hover_user_info_display(page):
    """첫 번째 사용자 이미지 호버 시 name: user1 텍스트 표시 확인"""
    page.goto(BASE_URL + "hovers")
    page.wait_for_load_state("domcontentloaded")
    page.locator("div.figure").nth(0).hover()
    expect(page.locator("div.figure").nth(0).locator(".figcaption")).to_be_visible(timeout=5000)
    expect(page.locator("div.figure").nth(0).locator(".figcaption")).to_contain_text("name: user1", timeout=5000)
    expect(page.locator("div.figure").nth(0).locator("a")).to_be_visible(timeout=5000)
