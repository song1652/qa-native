"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_85_xss_script_login (tc_85)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"


def test_tc_85_xss_script_login(page):
    """XSS 스크립트 입력으로 로그인 시도 시 실패 및 alert 미발생 확인"""
    alert_triggered = []
    page.on("dialog", lambda d: (alert_triggered.append(d.type), d.dismiss()))

    page.goto("https://the-internet.herokuapp.com/login")
    page.wait_for_load_state("domcontentloaded")
    page.locator("#username").fill("<script>alert('xss')</script>")
    page.locator("#password").fill("test")
    page.locator("button.radius").click()
    flash = page.locator("#flash")
    expect(flash).to_be_visible(timeout=5000)
    expect(flash).to_contain_text("Your username is invalid!")
    assert len(alert_triggered) == 0, "XSS alert was triggered unexpectedly"
