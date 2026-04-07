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
    """Shifting Content 이미지 페이지에서 이미지 표시 확인 (#content img.shift로 스코핑)"""
    page.goto("https://the-internet.herokuapp.com/shifting_content/image")
    page.wait_for_load_state("domcontentloaded")

    # Use #content img.shift to avoid strict mode (2 imgs: GitHub badge + content img)
    img = page.locator("#content img.shift")
    expect(img).to_be_visible(timeout=10000)

    # Record position before reload
    box_before = img.bounding_box()
    assert box_before is not None

    page.reload()
    page.wait_for_load_state("domcontentloaded")

    img_after = page.locator("#content img.shift")
    expect(img_after).to_be_visible(timeout=10000)
