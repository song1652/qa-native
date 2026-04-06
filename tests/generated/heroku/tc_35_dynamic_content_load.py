"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_35_dynamic_content_load (tc_35)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"


def test_dynamic_content_load(page):
    """동적 콘텐츠 로드 확인"""
    page.goto(BASE_URL + "dynamic_content")
    page.wait_for_load_state("networkidle")

    # 콘텐츠 행 확인 - div.row div.large-10 으로 각 행의 텍스트 컬럼
    # 동적 페이지이므로 정확한 개수 대신 최소 1개 이상 확인
    rows = page.locator("div.row div.large-10")
    count = rows.count()
    assert count >= 1, f"Expected at least 1 content row, got {count}"

    # 각 행에 텍스트가 존재하는지 확인
    for i in range(count):
        row = rows.nth(i)
        text = row.inner_text()
        assert len(text.strip()) > 0, f"Row {i} has no text"
