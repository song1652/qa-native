"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_48_nested_frames_bottom (tc_48)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from pathlib import Path

BASE_URL = "https://the-internet.herokuapp.com/"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_tc_48_nested_frames_bottom(page):
    """중첩 프레임 하단 프레임에서 BOTTOM 텍스트 확인"""
    page.goto("https://the-internet.herokuapp.com/nested_frames")
    page.wait_for_load_state("domcontentloaded")

    # Access the bottom frame via page.frame()
    bottom_frame = page.frame(url="**/frame_bottom")
    if bottom_frame is None:
        bottom_frame = page.frame(name="frame-bottom")

    if bottom_frame is not None:
        content = bottom_frame.locator("body").inner_text()
        assert "BOTTOM" in content
    else:
        # Fallback: use frame_locator
        frame_locator = page.frame_locator("frame[src*='bottom']")
        body_text = frame_locator.locator("body").inner_text()
        assert "BOTTOM" in body_text
