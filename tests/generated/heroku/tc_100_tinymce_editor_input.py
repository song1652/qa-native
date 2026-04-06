"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_79_tinymce_editor_input (tc_100)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from pathlib import Path

BASE_URL = "https://the-internet.herokuapp.com/"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_tc_79_tinymce_editor_input(page):
    """Type text into TinyMCE editor"""
    # TODO: Claude Code가 아래를 완성
    # 케이스 타입: structured
    # data_key: null
    # 전략: goto() → wait(iframe#mce_0_ifr) → fill(iframe#mce_0_ifr >> #tinymce)
    # 검증: text: Hello TinyMCE
    pass
