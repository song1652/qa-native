from playwright.sync_api import Page, expect

BASE_URL = "https://demoqa.com"


def test_nested_frames_show_parent_and_child_text(page: Page):
    page.goto(f"{BASE_URL}/nestedframes", wait_until="domcontentloaded")
    page.wait_for_timeout(2000)

    parent_frame = page.frame_locator("#frame1")
    expect(parent_frame.locator("body")).to_contain_text("Parent frame", timeout=10000)

    child_frame = parent_frame.frame_locator("iframe")
    expect(child_frame.locator("body")).to_contain_text("Child Iframe", timeout=10000)
