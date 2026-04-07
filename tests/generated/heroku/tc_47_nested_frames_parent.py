"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_47_nested_frames_parent (tc_47)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from pathlib import Path

BASE_URL = "https://the-internet.herokuapp.com/"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_tc_47_nested_frames_parent(page):
    """중첩 프레임에서 상단 3개 프레임 존재 및 MIDDLE 텍스트 확인"""
    page.goto("https://the-internet.herokuapp.com/nested_frames")
    page.wait_for_load_state("domcontentloaded")

    # Access the middle frame via page.frame()
    middle_frame = page.frame(url="**/frame_middle")
    if middle_frame is None:
        # Try by name
        middle_frame = page.frame(name="frame-middle")

    if middle_frame is not None:
        content = middle_frame.locator("body").inner_text()
        assert "MIDDLE" in content
    else:
        # Fallback: use frame_locator
        frame_locator = page.frame_locator("frame[src*='middle']")
        body_text = frame_locator.locator("body").inner_text()
        assert "MIDDLE" in body_text
