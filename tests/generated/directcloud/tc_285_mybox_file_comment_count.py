"""DirectCloud: tc_285 - 마이박스 — 파일 목록에 코멘트 수 표시 확인"""
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


def test_tc_285_mybox_file_comment_count(page):
    data = json.loads(TEST_DATA_PATH.read_text(encoding="utf-8"))
    creds = data["directcloud"]["valid_user"]
    login(page, creds["company"], creds["username"], creds["password"])
    dismiss_popups(page)

    # Navigate to mybox
    mybox = page.locator('li:has-text("My Box")')
    if mybox.count() > 0:
        mybox.first.click()
        page.wait_for_timeout(2000)
    dismiss_popups(page)

    # Look for comment count icon or badge in file rows
    comment_count = page.locator(
        '[class*="comment-count"], [class*="comment_count"], '
        '.badge[class*="comment"], [class*="icon-comment"] + span, '
        'td [class*="comment"], li [class*="comment"][class*="count"]'
    )
    assert comment_count.count() > 0, "파일 목록에 코멘트 수 배지가 표시되지 않습니다"
    assert comment_count.first.is_visible(), "코멘트 수 배지가 보이지 않습니다"
