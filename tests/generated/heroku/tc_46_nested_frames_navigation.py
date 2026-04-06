from pathlib import Path
from playwright.sync_api import Page, expect

BASE_URL = "https://the-internet.herokuapp.com/"
TEST_DATA_PATH = (
    Path(__file__).resolve().parent.parent.parent.parent
    / "config" / "test_data.json"
)


def test_nested_frames_navigation(page: Page) -> None:
    page.goto("https://the-internet.herokuapp.com/frames")
    page.wait_for_load_state("domcontentloaded")

    page.get_by_role("link", name="Nested Frames").click()
    page.wait_for_load_state("domcontentloaded")

    expect(page).to_have_url(
        "https://the-internet.herokuapp.com/nested_frames"
    )

    frames = page.frames
    assert len(frames) > 1, "Nested frame structure should be present"
