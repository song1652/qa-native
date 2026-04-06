"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_22_ab_test_content_variation (tc_22)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_tc_22_ab_test_content_variation(page):
    """A/B 테스트 콘텐츠 변형 확인"""
    page.goto(BASE_URL + "abtest")
    expect(page.locator("body")).to_be_visible()

    heading = page.locator("h3")
    expect(heading).to_be_visible(timeout=10000)
    heading_text = heading.inner_text()
    assert "A/B Test" in heading_text, f"Expected 'A/B Test' in heading, got: {heading_text}"

    # Verify content area exists
    content_area = page.locator("div.example")
    expect(content_area).to_be_visible()
