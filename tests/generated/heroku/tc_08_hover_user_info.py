"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_08_hover_user_info (tc_08)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from pathlib import Path

BASE_URL = "https://the-internet.herokuapp.com/"
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_tc_08_hover_user_info(page):
    """사용자 이미지 hover 시 figcaption이 나타나고 user1/user2 이름과 View profile 링크가 포함된다"""
    page.goto("https://the-internet.herokuapp.com/hovers")

    figures = page.locator(".figure")

    for i, expected_user in enumerate(["user1", "user2"]):
        figure = figures.nth(i)
        figure.locator("img").hover()
        page.wait_for_timeout(300)

        caption = figure.locator(".figcaption")
        caption.wait_for(state="visible", timeout=5000)
        caption_text = caption.inner_text()
        assert expected_user in caption_text, f"Expected '{expected_user}' in caption, got: {caption_text}"
        assert "View profile" in caption_text, f"Expected 'View profile' link in caption {i+1}"
