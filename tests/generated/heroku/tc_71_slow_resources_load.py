"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_71_slow_resources_load (tc_71)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_tc_71_slow_resources_load(page):
    """느린 리소스 페이지 로드 대기 (30초) 후 정상 표시 확인"""
    page.goto("https://the-internet.herokuapp.com/slow", timeout=30000)
    page.wait_for_load_state("domcontentloaded", timeout=30000)

    heading = page.locator("h3")
    expect(heading).to_be_visible(timeout=30000)
    expect(heading).to_contain_text("Slow Resources", timeout=30000)
