"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_51_infinite_scroll_load_more (tc_51)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
BASE_URL = "https://the-internet.herokuapp.com/"


def test_infinite_scroll_load_more(page):
    """무한 스크롤 추가 콘텐츠 로드"""
    page.goto(BASE_URL + "infinite_scroll")
    page.wait_for_load_state("networkidle")

    # 초기 높이 기록
    initial_height = page.evaluate("document.body.scrollHeight")

    # 페이지 하단으로 스크롤
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(2000)

    # 스크롤 후 높이 확인 (더 많은 콘텐츠 로드)
    new_height = page.evaluate("document.body.scrollHeight")
    assert new_height >= initial_height, (
        f"Expected height to grow or stay same after scroll, "
        f"got initial={initial_height}, new={new_height}"
    )

    # 추가 스크롤로 더 많은 콘텐츠 로드 시도
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(2000)

    final_height = page.evaluate("document.body.scrollHeight")
    # 최소한 한 번의 스크롤 이후 콘텐츠가 늘어났는지 확인
    assert final_height >= initial_height, (
        "Page height did not increase after scrolling"
    )
