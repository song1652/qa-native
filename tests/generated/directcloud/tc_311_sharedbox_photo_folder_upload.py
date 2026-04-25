"""DirectCloud: tc_311 - 공유박스 — 포토 폴더에 이미지 파일 업로드"""
import json
from pathlib import Path

BASE_URL = "https://web.directcloud.jp/login"
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"
TEST_IMAGE_PATH = PROJECT_ROOT / "tests" / "fixtures" / "test_image.png"


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


def test_tc_311_sharedbox_photo_folder_upload(page):
    with open(TEST_DATA_PATH, encoding="utf-8") as f:
        data = json.load(f)
    creds = data["directcloud"]["valid_user"]
    login(page, creds["company"], creds["username"], creds["password"])
    dismiss_popups(page)

    # 공유박스 사이드바 클릭
    sharedbox_nav = page.locator('li#sharedbox')
    assert sharedbox_nav.count() > 0, "공유박스 메뉴를 찾을 수 없습니다"
    sharedbox_nav.first.click(timeout=5000)
    page.wait_for_timeout(1500)
    dismiss_popups(page)

    # 사이드바 트리에서 Photo 하위 항목 직접 클릭 (파일 목록보다 신뢰성 높음)
    photo_nav = page.locator(
        'li#sharedbox li:has-text("Photo"), '
        'li#sharedbox li:has-text("photo"), '
        'li#sharedbox li:has-text("フォト"), '
        'li#sharedbox li:has-text("사진")'
    )
    assert photo_nav.count() > 0, "공유박스 사이드바에서 Photo 항목을 찾을 수 없습니다"
    photo_nav.first.click(timeout=5000)
    page.wait_for_timeout(1500)
    dismiss_popups(page)

    # Photo 폴더 진입 확인 — URL에 sharedbox 경로 포함
    current_url = page.url
    assert "sharedbox" in current_url, f"Photo 폴더 진입 실패, 현재 URL: {current_url}"

    # 파일 업로드 input 확인 (필수 — 없으면 실패)
    upload_input = page.locator('input[type="file"]')
    assert upload_input.count() > 0, "업로드 input[type=file]을 찾을 수 없습니다"

    # 파일 주입
    upload_input.first.set_input_files(str(TEST_IMAGE_PATH))
    page.wait_for_timeout(2000)
    dismiss_popups(page)

    # 업로드 완료 대기 — 프로그레스바 사라질 때까지 최대 20초
    try:
        progress = page.locator(
            '[class*="progress"], [class*="upload-progress"], '
            '[class*="uploadProgress"], .progress-bar'
        )
        if progress.count() > 0:
            progress.first.wait_for(state='hidden', timeout=20000)
    except Exception:
        pass
    page.wait_for_timeout(2000)
    dismiss_popups(page)

    # 업로드된 파일명이 목록에 반드시 표시돼야 통과
    uploaded = page.locator('text=test_image.png')
    assert uploaded.count() > 0, "업로드 후 파일 목록에 test_image.png가 표시되지 않습니다"
    assert uploaded.first.is_visible(), "test_image.png가 목록에 있으나 보이지 않습니다"
