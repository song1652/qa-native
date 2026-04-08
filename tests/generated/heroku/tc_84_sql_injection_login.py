"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_84_sql_injection_login (tc_84)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"


def test_tc_84_sql_injection_login(page):
    """SQL Injection 문자열로 로그인 시도 시 실패 확인"""
    page.goto("https://the-internet.herokuapp.com/login")
    page.wait_for_load_state("domcontentloaded")
    page.locator("#username").fill("' OR '1'='1")
    page.locator("#password").fill("' OR '1'='1")
    page.locator("button.radius").click()
    flash = page.locator("#flash")
    expect(flash).to_be_visible(timeout=5000)
    expect(flash).to_contain_text("Your username is invalid!")
