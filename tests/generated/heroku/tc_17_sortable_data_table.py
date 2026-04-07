"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_17_sortable_data_table (tc_17)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from pathlib import Path

BASE_URL = "https://the-internet.herokuapp.com/"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_tc_17_sortable_data_table(page):
    """테이블1의 Last Name 헤더 클릭 후 정렬 확인 (headerSortDown 클래스)"""
    # TODO: Claude Code가 아래를 완성
    # 케이스 타입: structured
    # data_key: null
    # 전략: goto() → click(#table1 thead th >> nth=0)
    # 검증: class_contains: #table1 th:nth-child(1) has headerSortDown
    pass
