from pathlib import Path
from playwright.sync_api import Page

BASE_URL = "https://the-internet.herokuapp.com/"
TEST_DATA_PATH = (
    Path(__file__).resolve().parent.parent.parent.parent
    / "config" / "test_data.json"
)


def test_nested_frames_middle_text(page: Page) -> None:
    page.goto("https://the-internet.herokuapp.com/nested_frames")
    page.wait_for_load_state("domcontentloaded")

    # Wait for frames to load
    page.wait_for_timeout(1000)

    all_frames = page.frames
    # Find the frame that contains "MIDDLE" text
    middle_frame = None
    for frame in all_frames:
        try:
            content = frame.content()
            if "MIDDLE" in content:
                middle_frame = frame
                break
        except Exception:
            continue

    assert middle_frame is not None, (
        "MIDDLE frame text should be found in nested frames"
    )
