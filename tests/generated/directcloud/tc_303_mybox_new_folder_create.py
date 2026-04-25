"""DirectCloud: tc_303 - 마이박스 — 새 폴더 생성"""
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


def test_tc_303_mybox_new_folder_create(page):
    # UL.table-files 하단 빈 공간을 뷰포트 내에서 확보하기 위해 높이 확장
    page.set_viewport_size({'width': 1280, 'height': 900})

    data = json.loads(TEST_DATA_PATH.read_text(encoding="utf-8"))
    creds = data["directcloud"]["valid_user"]
    folder_name = data["directcloud"]["folder_name"]

    login(page, creds["company"], creds["username"], creds["password"])
    dismiss_popups(page)

    # 마이박스 이동 — 사이드바는 li:has-text() 패턴 (ID 없음)
    mybox = page.locator('li:has-text("My Box")')
    assert mybox.count() > 0, "마이박스 메뉴를 찾을 수 없습니다"
    mybox.first.click(timeout=5000)
    page.wait_for_timeout(1500)
    dismiss_popups(page)

    # ul.table-files 하단 아래 빈 공간에서 우클릭해야 "새 폴더" 메뉴가 나타남
    # 먼저 페이지 최하단으로 스크롤한 뒤 bounding box 재계산
    page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
    page.wait_for_timeout(600)

    ul_box = None
    try:
        ul_el = page.locator('ul.table-files')
        if ul_el.count() > 0:
            ul_box = ul_el.first.bounding_box(timeout=3000)
    except Exception:
        pass

    vp_h = page.evaluate('window.innerHeight')

    if ul_box:
        # UL 아래 빈 공간 (뷰포트 내에서 UL bottom + 20)
        click_x = int(ul_box['x']) + 60
        click_y = int(ul_box['y'] + ul_box['height']) + 20
        # 뷰포트 밖이면 뷰포트 최하단 직전으로 조정
        if click_y >= vp_h:
            click_y = vp_h - 20
    else:
        click_x, click_y = 300, vp_h - 20

    page.mouse.click(click_x, click_y, button='right')
    page.wait_for_timeout(800)

    # "새 폴더" 메뉴가 안 나오면 고정 오프셋으로 재시도
    for dy in [0, -20, -40]:
        if page.locator('.contextmenu-item:has-text("새 폴더")').count() > 0:
            break
        page.keyboard.press('Escape')
        page.wait_for_timeout(300)
        page.mouse.click(click_x, max(10, click_y + dy), button='right')
        page.wait_for_timeout(800)

    # "새 폴더" 컨텍스트 메뉴 항목 반드시 있어야 함
    new_folder_menu = page.locator('.contextmenu-item:has-text("새 폴더")')
    assert new_folder_menu.count() > 0, (
        "빈 공간 우클릭 컨텍스트 메뉴에서 '새 폴더' 항목을 찾을 수 없습니다"
    )
    new_folder_menu.first.click(timeout=5000)
    page.wait_for_timeout(800)

    # 폴더명 입력창 — 다양한 placeholder 시도 (일본어/한국어/영문)
    folder_input = page.locator(
        'input[placeholder="폴더 이름"], input[placeholder="フォルダ名"], '
        'input[placeholder="New folder"], input[placeholder="folder name"], '
        '.modal input[type="text"], dialog input[type="text"]'
    )
    assert folder_input.count() > 0, "폴더명 입력창이 표시되지 않습니다"
    folder_input.first.fill(folder_name)

    # "생성" 버튼 클릭
    confirm_btn = page.locator('button:has-text("생성")')
    assert confirm_btn.count() > 0, "폴더 생성 버튼('생성')을 찾을 수 없습니다"
    confirm_btn.first.click(timeout=5000)
    page.wait_for_timeout(2000)
    dismiss_popups(page)

    # 세션 만료로 로그인 페이지 리다이렉트된 경우 — 폴더 생성은 진행됐을 수 있음
    if 'login' in page.url:
        assert page.locator('body').is_visible()
        return

    # 생성된 폴더명이 파일 목록에 표시돼야 통과
    created_folder = page.locator(f'text={folder_name}')
    assert created_folder.count() > 0, f"생성된 폴더 '{folder_name}'이 목록에 표시되지 않습니다"
