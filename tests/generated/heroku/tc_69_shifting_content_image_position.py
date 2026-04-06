"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_69_shifting_content_image_position (tc_69)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from pathlib import Path

from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_tc_69_shifting_content_image_position(page):
    """Shifting Content 이미지 위치 변화"""
    page.goto(BASE_URL + "shifting_content/image")
    page.wait_for_load_state("domcontentloaded")

    img = page.locator("img").first
    expect(img).to_be_visible(timeout=10000)

    # Get bounding box to verify image is rendered with a position
    bbox = img.bounding_box()
    assert bbox is not None, "Expected image to have a bounding box"
    assert bbox["width"] > 0 and bbox["height"] > 0, (
        f"Expected image to have dimensions, got: {bbox}"
    )
