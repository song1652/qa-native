"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_25_normal_image_load (tc_25)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_tc_25_normal_image_load(page):
    """정상 이미지 로드 확인"""
    page.goto(BASE_URL + "broken_images")
    expect(page.locator("body")).to_be_visible()
    page.wait_for_load_state("networkidle", timeout=15000)

    natural_widths = page.evaluate("""
        () => {
            const imgs = Array.from(document.querySelectorAll('#content img'));
            return imgs.map(img => img.naturalWidth);
        }
    """)

    loaded = [w for w in natural_widths if w > 0]
    assert len(loaded) >= 1, f"Expected at least 1 loaded image, all widths: {natural_widths}"
