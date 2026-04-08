from playwright.sync_api import Page, expect

BASE_URL = "https://demoqa.com"


def test_broken_links_images(page: Page):
    page.goto(BASE_URL + "/broken", wait_until="domcontentloaded")
    page.wait_for_timeout(2000)

    # Click the valid link
    valid_link = page.get_by_text("Click Here for Valid Link")
    expect(valid_link).to_be_visible(timeout=10000)

    with page.expect_response(lambda r: r.status == 200) as response_info:
        valid_link.click()
        page.wait_for_load_state("domcontentloaded")
        page.wait_for_timeout(2000)

    response = response_info.value
    assert response.status == 200, f"Expected 200 but got {response.status}"
    expect(page.locator("body")).to_be_visible(timeout=5000)
