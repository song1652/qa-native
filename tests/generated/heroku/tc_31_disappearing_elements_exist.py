"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_31_disappearing_elements_exist (tc_31)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_tc_31_disappearing_elements_exist(page):
    """사라지는 요소 존재 확인"""
    page.goto(BASE_URL + "disappearing_elements")
    expect(page.locator("body")).to_be_visible()

    # Nav links are inside ul > li > a
    nav_links = page.locator("ul li a")
    count = nav_links.count()
    # Gallery is random — always at least 4 stable links
    assert count >= 4, f"Expected >= 4 nav links, got {count}"

    # Verify the stable links exist
    link_texts = [nav_links.nth(i).inner_text() for i in range(count)]
    for expected in ["Home", "About", "Contact Us", "Portfolio"]:
        assert expected in link_texts, f"Expected '{expected}' in nav links, got: {link_texts}"
