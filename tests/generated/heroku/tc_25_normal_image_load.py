"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_25_normal_image_load (tc_25)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
BASE_URL = "https://the-internet.herokuapp.com/"


def test_tc_25_normal_image_load(page):
    """정상 로드된 이미지가 최소 1개 존재하는지 확인"""
    page.goto("https://the-internet.herokuapp.com/broken_images")
    page.wait_for_load_state("networkidle")
    normal_count = page.evaluate("""() => {
        const imgs = Array.from(document.querySelectorAll('div.example img'));
        return imgs.filter(img => img.naturalWidth > 0).length;
    }""")
    assert normal_count >= 1, f"Expected at least 1 normal image, got {normal_count}"
