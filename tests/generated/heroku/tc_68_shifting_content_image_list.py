"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_68_shifting_content_image_list (tc_68)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from pathlib import Path

from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_tc_68_shifting_content_image_list(page):
    """Shifting Content 이미지 목록 확인"""
    page.goto(BASE_URL + "shifting_content")
    page.wait_for_load_state("domcontentloaded")

    # Verify example links exist
    expect(page.locator("a[href*='shifting_content/menu']")).to_be_visible(
        timeout=10000
    )
    expect(page.locator("a[href*='shifting_content/image']")).to_be_visible(
        timeout=10000
    )
    expect(page.locator("a[href*='shifting_content/list']")).to_be_visible(
        timeout=10000
    )
