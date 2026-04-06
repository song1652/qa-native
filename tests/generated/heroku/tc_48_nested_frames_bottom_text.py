"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_48_nested_frames_bottom_text (tc_48)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
BASE_URL = "https://the-internet.herokuapp.com/"


def test_nested_frames_bottom_text(page):
    """중첩 프레임 하단 프레임 텍스트 확인"""
    page.goto(BASE_URL + "nested_frames")
    page.wait_for_load_state("load")

    # 모든 프레임에서 BOTTOM 텍스트 찾기
    bottom_found = False
    for frame in page.frames:
        try:
            content = frame.evaluate(
                "document.body ? document.body.innerText : ''"
            )
            if "BOTTOM" in content:
                bottom_found = True
                break
        except Exception:
            continue

    assert bottom_found, (
        "BOTTOM text not found in any frame"
    )
