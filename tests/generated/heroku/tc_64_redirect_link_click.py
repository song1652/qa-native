"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_64_redirect_link_click (tc_64)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from pathlib import Path

BASE_URL = "https://the-internet.herokuapp.com/"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_tc_64_redirect_link_click(page):
    """리다이렉트 링크 클릭"""
    page.goto(BASE_URL + "redirector")

    page.locator("a", has_text="here").click()
    page.wait_for_load_state("domcontentloaded")

    assert "/status_codes" in page.url, (
        f"Expected redirect to /status_codes, got: {page.url}"
    )
