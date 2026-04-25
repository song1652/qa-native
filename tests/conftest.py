import json
import pytest
from pathlib import Path
from datetime import datetime
from playwright.sync_api import sync_playwright


@pytest.fixture(scope="session")
def browser_instance():
    import os
    headless = os.environ.get("HEADED", "0") != "1"
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        yield browser
        browser.close()


@pytest.fixture
def page(browser_instance):
    context = browser_instance.new_context()
    page = context.new_page()
    # DirectCloud 세션 충돌 dialog 자동 수락
    page.on("dialog", lambda dialog: dialog.accept())
    yield page
    # 테스트 종료 후 세션 명시적 정리 (다음 테스트 로그인 충돌 방지)
    try:
        page.goto("https://web.directcloud.jp/logout", timeout=5000)
    except Exception:
        pass
    context.close()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        page = item.funcargs.get("page")
        if page:
            shot_dir = Path("tests/screenshots")
            shot_dir.mkdir(parents=True, exist_ok=True)
            # 그룹 네임스페이스: tests/generated/{group}/{file}.py → group 추출
            test_file = Path(item.fspath)
            group = test_file.parent.name if test_file.parent.name != "generated" else "default"
            path = shot_dir / f"{group}__{item.name}.png"
            try:
                page.screenshot(path=str(path))
                # 메타데이터 저장 (힐링 시 URL·타임스탬프 활용)
                meta_path = shot_dir / f"{group}__{item.name}.meta.json"
                meta = {
                    "test_name": item.name,
                    "group": group,
                    "url": page.url,
                    "timestamp": datetime.now().isoformat(),
                    "screenshot_path": str(path),
                }
                meta_path.write_text(
                    json.dumps(meta, ensure_ascii=False, indent=2),
                    encoding="utf-8",
                )
                print(f"\n스크린샷 저장: {path}")
            except Exception:
                pass
