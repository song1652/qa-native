"""
자동 생성된 Playwright 테스트 코드
URL: https://web.directcloud.jp/login
케이스: tc_05_stay_signed_in_checkbox (tc_05_stay_signed_in_checkbox)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from pathlib import Path

BASE_URL = "https://web.directcloud.jp/login"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_tc_05_stay_signed_in_checkbox(page):
    """Stay signed in 체크박스 토글"""
    page.goto(BASE_URL)

    checkbox = page.locator('input[type="checkbox"]')
    assert checkbox.is_visible()

    initial_checked = checkbox.is_checked()

    checkbox.click()
    assert checkbox.is_checked() != initial_checked

    checkbox.click()
    assert checkbox.is_checked() == initial_checked
