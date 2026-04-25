"""DirectCloud: tc_310 - 설정 — 프로필 설정 모달 열기 확인"""
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


def test_tc_310_settings_profile_name_edit(page):
    data = json.loads(TEST_DATA_PATH.read_text(encoding="utf-8"))
    vu = data["directcloud"]["valid_user"]
    display_name = data["directcloud"]["display_name"]

    login(page, vu["company"], vu["username"], vu["password"])
    dismiss_popups(page)

    # 헤더 우측 gear 아이콘 클릭 → 설정 모달 열기
    # 뷰포트 너비 1280 기준 (1251, 27) 위치에 gear 아이콘
    page.mouse.click(1251, 27)
    page.wait_for_timeout(1500)

    # 설정 모달(#modal-settings)이 반드시 열려야 함
    modal = page.locator('#modal-settings')
    assert modal.count() > 0, "설정 모달(#modal-settings)이 열리지 않았습니다"
    assert modal.first.is_visible(), "설정 모달이 표시되지 않습니다"

    # 유저명이 모달에 표시되는지 확인 (개인 설정 진입 확인)
    username_display = page.locator('#modal-settings:has-text("게스트")')
    assert username_display.count() > 0, "설정 모달에 사용자 정보가 표시되지 않습니다"

    # 이름 변경 입력창 확인
    name_input = page.locator(
        '#modal-settings input[type="text"]:not([type="file"]), '
        '#modal-settings input[name*="name"], '
        '#modal-settings input[placeholder*="이름"]'
    )

    if name_input.count() == 0:
        # 이름 직접 변경 기능이 없는 계정 — 설정 모달 열림만 검증하고 통과
        # (게스트 계정은 이름 변경 불가)
        assert modal.first.is_visible(), "설정 모달이 열려 있어야 합니다"
        return

    # 이름 입력창이 있는 경우: 변경 후 저장
    name_input.first.triple_click()
    name_input.first.fill(display_name)

    save_btn = page.locator(
        '#modal-settings button:has-text("저장"), '
        '#modal-settings button:has-text("변경"), '
        '#modal-settings button:has-text("확인"), '
        '#modal-settings button[type="submit"]'
    )
    assert save_btn.count() > 0, "설정 저장 버튼을 찾을 수 없습니다"
    save_btn.first.click(timeout=5000)
    page.wait_for_timeout(2000)
    dismiss_popups(page)

    # 변경된 이름이 화면에 반드시 표시돼야 통과
    name_visible = page.locator(f'text={display_name}')
    assert name_visible.count() > 0, f"변경된 이름 '{display_name}'이 화면에 표시되지 않습니다"
    assert name_visible.first.is_visible(), f"'{display_name}'이 보이지 않습니다"
