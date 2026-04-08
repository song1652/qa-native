"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_18_dynamic_loading_wait (tc_18)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from pathlib import Path

BASE_URL = "https://the-internet.herokuapp.com/"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_tc_18_dynamic_loading_wait(page):
    """Start 버튼 클릭 후 로딩 완료 대기, Hello World! 텍스트 표시 확인"""
    # TODO: Claude Code가 아래를 완성
    # 케이스 타입: structured
    # data_key: null
    # 전략: goto() → click(#start button) → wait(#finish)
    # 검증: text_contains: #finish: Hello World!
    pass
