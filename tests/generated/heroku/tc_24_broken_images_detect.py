"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_24_broken_images_detect (tc_24)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
BASE_URL = "https://the-internet.herokuapp.com/"


def test_tc_24_broken_images_detect(page):
    """깨진 이미지 존재 감지 (naturalWidth=0인 이미지 확인)"""
    page.goto("https://the-internet.herokuapp.com/broken_images")
    page.wait_for_load_state("networkidle")
    broken_count = page.evaluate("""() => {
        const imgs = Array.from(document.querySelectorAll('div.example img'));
        return imgs.filter(img => img.naturalWidth === 0).length;
    }""")
    assert broken_count >= 1, f"Expected at least 1 broken image, got {broken_count}"
