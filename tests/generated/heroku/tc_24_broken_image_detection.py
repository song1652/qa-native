"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_24_broken_image_detection (tc_24)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_tc_24_broken_image_detection(page):
    """깨진 이미지 감지"""
    page.goto(BASE_URL + "broken_images")
    expect(page.locator("body")).to_be_visible()
    page.wait_for_load_state("networkidle", timeout=15000)

    # Get naturalWidth for all images via JS
    natural_widths = page.evaluate("""
        () => {
            const imgs = Array.from(document.querySelectorAll('#content img'));
            return imgs.map(img => img.naturalWidth);
        }
    """)

    assert len(natural_widths) >= 3, f"Expected >= 3 images, got {len(natural_widths)}"
    broken = [w for w in natural_widths if w == 0]
    assert len(broken) > 0, f"Expected at least 1 broken image, all widths: {natural_widths}"
