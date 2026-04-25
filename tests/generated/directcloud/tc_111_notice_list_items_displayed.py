"""DirectCloud: tc_111 - Notice 페이지 목록 항목 표시 확인"""
import json
from pathlib import Path

BASE_URL = "https://web.directcloud.jp/login"
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def login(page, company_code, user_id, password):
    page.goto(BASE_URL)
    page.wait_for_timeout(1000)
    page.fill('[name="company_code"]', company_code)
    page.fill('[name="id"]', user_id)
    page.fill('[name="password"]', password)
    page.click('#new_btn_login')
    try:
        page.wait_for_url("**/mybox/**", timeout=20000)
    except Exception:
        page.goto(BASE_URL)
        page.wait_for_timeout(3000)
        page.fill('[name="company_code"]', company_code)
        page.fill('[name="id"]', user_id)
        page.fill('[name="password"]', password)
        page.click('#new_btn_login')
        page.wait_for_url("**/mybox/**", timeout=20000)


def dismiss_popups(page):
    page.keyboard.press('Escape')
    page.wait_for_timeout(300)
    try:
        page.evaluate("""() => {
            const overlays = document.querySelectorAll('div[class*="sc-T"]');
            overlays.forEach(el => {
                const style = window.getComputedStyle(el);
                if (style.position === 'fixed' || parseInt(style.zIndex) > 100) el.remove();
            });
        }""")
    except Exception:
        pass
    page.wait_for_timeout(200)


def test_tc_111_notice_list_items_displayed(page):
    with open(TEST_DATA_PATH, 'r', encoding='utf-8') as f:
        test_data = json.load(f)
    creds = test_data["directcloud"]["valid_user"]
    login(page, creds["company"], creds["username"], creds["password"])
    dismiss_popups(page)

    page.goto("https://web.directcloud.jp/notice")
    page.wait_for_timeout(2000)
    dismiss_popups(page)

    assert "notice" in page.url

    # Notice DOM: 목록에 listitem이 있는지 확인 (제목/구분/날짜 컬럼 포함)
    assert page.locator(':text("제목")').count() > 0
    list_items = page.locator('ul li')
    assert list_items.count() > 0

    assert page.locator('body').is_visible()
