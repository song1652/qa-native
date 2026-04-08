from playwright.sync_api import Page, expect

BASE_URL = "https://demoqa.com"


def test_large_frame_contains_sample_page_text(page: Page):
    page.goto(f"{BASE_URL}/frames", wait_until="domcontentloaded")
    page.wait_for_timeout(2000)

    frame = page.frame_locator("#frame1")
    expect(frame.locator("h1")).to_contain_text("This is a sample page", timeout=10000)
