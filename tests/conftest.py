import pytest
from pathlib import Path
from playwright.sync_api import sync_playwright


@pytest.fixture(scope="session")
def browser_instance():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        yield browser
        browser.close()


@pytest.fixture
def page(browser_instance):
    context = browser_instance.new_context()
    page = context.new_page()
    yield page
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
            path = shot_dir / f"{item.name}.png"
            try:
                page.screenshot(path=str(path))
                print(f"\n스크린샷 저장: {path}")
            except Exception:
                pass
