"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_47_nested_frames_parent (tc_47)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
BASE_URL = "https://the-internet.herokuapp.com/"


def test_nested_frames_parent(page):
    """중첩 프레임 구조 확인"""
    page.goto(BASE_URL + "nested_frames")
    page.wait_for_load_state("load")

    # frameset 구조 확인 - evaluate로 frame 수 확인
    frame_count = page.evaluate("window.frames.length")
    assert frame_count >= 1, f"Expected at least 1 frame, got {frame_count}"

    # 상단 프레임(frame-top)의 내부 프레임들 확인
    # nested_frames 구조: top (left, middle, right) + bottom
    frames = page.frames
    assert len(frames) >= 2, (
        f"Expected at least 2 frames, got {len(frames)}"
    )

    # MIDDLE 텍스트가 있는 프레임 찾기
    middle_found = False
    for frame in frames:
        try:
            content = frame.evaluate(
                "document.body ? document.body.innerText : ''"
            )
            if "MIDDLE" in content:
                middle_found = True
                break
        except Exception:
            continue

    assert middle_found, "MIDDLE frame content not found"
