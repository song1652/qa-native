from pathlib import Path
from playwright.sync_api import Page

BASE_URL = "https://the-internet.herokuapp.com/"
TEST_DATA_PATH = (
    Path(__file__).resolve()
    .parent.parent.parent.parent
    / "config" / "test_data.json"
)


def test_javascript_error_console_check(page: Page):
    """JavaScript 에러 페이지 콘솔 에러 확인"""
    js_errors = []

    page.on("pageerror", lambda exc: js_errors.append(str(exc)))

    page.goto("https://the-internet.herokuapp.com/javascript_error")
    page.wait_for_load_state("domcontentloaded")
    page.wait_for_timeout(2000)

    assert len(js_errors) > 0, (
        "Expected JavaScript console error, but none were captured"
    )
    assert any(
        "Cannot read properties of undefined" in err or "Cannot read" in err
        for err in js_errors
    ), (
        f"Expected 'Cannot read properties of undefined' in errors, "
        f"got: {js_errors}"
    )
