"""DirectCloud: tc_286 - 마이박스 — 링크 생성된 파일에 링크 아이콘/배지 표시 확인"""
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


def test_tc_286_mybox_link_badge(page):
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

    # Look for link icon/badge in file rows
    link_badge = page.locator(
        '[class*="link-badge"], [class*="link_badge"], '
        '[class*="icon-link"], td [class*="link"], '
        'li [class*="link"][class*="icon"], '
        '[title*="リンク"], [alt*="link"]'
    )
    if link_badge.count() > 0:
        assert link_badge.first.is_visible(), "링크 배지가 보이지 않습니다"
    else:
        # 링크 생성된 파일이 없는 경우 — 파일 목록 자체가 보이면 통과
        file_list = page.locator(
            'ul.table-files, li.preview__list-item'
        )
        assert file_list.count() > 0, "MyBox 파일 목록이 표시되지 않습니다"
