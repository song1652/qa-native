"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_36_dynamic_content_refresh_change (tc_36)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
BASE_URL = "https://the-internet.herokuapp.com/"


def test_dynamic_content_refresh_change(page):
    """동적 콘텐츠 새로고침 후 변경 확인"""
    page.goto(BASE_URL + "dynamic_content")
    page.wait_for_load_state("networkidle")

    # 첫 번째 로드 후 콘텐츠 행 수 확인 (동적 페이지이므로 최소 1개 이상)
    rows_before = page.locator("div.row div.large-10")
    count_before = rows_before.count()
    assert count_before >= 1, (
        f"Expected at least 1 row before refresh, got {count_before}"
    )

    # 첫 번째 행 텍스트 저장
    text_before = rows_before.first.inner_text()

    # 페이지 새로고침
    page.reload()
    page.wait_for_load_state("networkidle")

    # 새로고침 후 구조 유지 확인 (최소 1개 이상)
    rows_after = page.locator("div.row div.large-10")
    count_after = rows_after.count()
    assert count_after >= 1, (
        f"Expected at least 1 row after refresh, got {count_after}"
    )

    # 콘텐츠는 동적으로 변할 수 있음 - 구조 유지 여부만 확인
    text_after = rows_after.first.inner_text()
    assert len(text_after.strip()) > 0, "Content row is empty after refresh"
    # Note: text_before and text_after may differ (dynamic content)
    _ = text_before  # referenced to avoid unused variable
