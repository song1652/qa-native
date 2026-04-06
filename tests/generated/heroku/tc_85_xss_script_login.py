from playwright.sync_api import Page, expect

BASE_URL = "https://the-internet.herokuapp.com/"


def test_xss_script_login(page: Page):
    alert_triggered = []
    page.on("dialog", lambda d: (alert_triggered.append(True), d.dismiss()))

    page.goto(BASE_URL + "login")
    page.wait_for_load_state("domcontentloaded")

    page.locator("#username").fill("<script>alert('xss')</script>")
    page.locator("#password").fill("test")
    page.locator("button[type='submit']").click()

    expect(page.locator("#flash")).to_contain_text(
        "Your username is invalid!", timeout=10000
    )
    assert len(alert_triggered) == 0, (
        "XSS alert dialog was triggered unexpectedly"
    )
