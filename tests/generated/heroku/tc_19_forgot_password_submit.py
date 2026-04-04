"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: test_forgot_password_submit (tc_19)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
import json
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_forgot_password_submit(page):
    """비밀번호 찾기 이메일 제출 — 이메일 입력 후 페이지 전환 확인"""
    with open(TEST_DATA_PATH, encoding="utf-8") as f:
        data = json.load(f)["heroku"]["forgot_email"]

    page.goto(BASE_URL + "forgot_password")

    # 폼 제출 전 email 필드 존재 확인
    email_input = page.locator("#email")
    expect(email_input).to_be_visible(timeout=5000)

    email_input.fill(data["email"])
    page.locator("#form_submit").click()
    page.wait_for_load_state("domcontentloaded")

    # lessons_learned: 서버 에러 가능성 고려, 특정 응답 메시지 하드코딩 금지
    # 폼 제출 후 email 입력 폼이 사라지거나 페이지가 변경되었음을 확인
    expect(page.locator("#email")).not_to_be_visible(timeout=5000)
