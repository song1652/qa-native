"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_15_file_upload (tc_15)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from pathlib import Path

BASE_URL = "https://the-internet.herokuapp.com/"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_tc_15_file_upload(page):
    """임시 파일 생성 후 업로드, 완료 메시지와 파일명 확인"""
    # TODO: Claude Code가 아래를 완성
    # 케이스 타입: structured
    # data_key: null
    # 전략: goto() → fill(#file-upload) → click(#file-submit)
    # 검증: text_contains: File Uploaded!
    pass
