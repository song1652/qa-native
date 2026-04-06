"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_71_slow_resource_load_wait (tc_71)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from pathlib import Path

from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_tc_71_slow_resource_load_wait(page):
    """느린 리소스 로드 대기"""
    # Extended timeout because /slow intentionally delays resources
    page.goto(BASE_URL + "slow", timeout=60000, wait_until="domcontentloaded")

    heading = page.locator("h3")
    expect(heading).to_be_visible(timeout=30000)
    expect(heading).to_contain_text("Slow Resources", ignore_case=True)
