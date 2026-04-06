"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_32_disappearing_elements_refresh (tc_32)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_tc_32_disappearing_elements_refresh(page):
    """사라지는 요소 새로고침 후 변화 확인"""
    page.goto(BASE_URL + "disappearing_elements")
    expect(page.locator("body")).to_be_visible()

    # Check count before refresh
    nav_links = page.locator("ul li a")
    count_before = nav_links.count()
    assert count_before >= 4, f"Expected >= 4 nav links before refresh, got {count_before}"

    # Reload page
    page.reload()
    expect(page.locator("body")).to_be_visible()

    # Check count after refresh — Gallery may appear/disappear
    nav_links_after = page.locator("ul li a")
    count_after = nav_links_after.count()
    assert count_after >= 4, f"Expected >= 4 nav links after refresh, got {count_after}"
