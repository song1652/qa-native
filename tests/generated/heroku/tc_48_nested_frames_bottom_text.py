from pathlib import Path
from playwright.sync_api import Page

BASE_URL = "https://the-internet.herokuapp.com/"
TEST_DATA_PATH = (
    Path(__file__).resolve().parent.parent.parent.parent
    / "config" / "test_data.json"
)


def test_nested_frames_bottom_text(page: Page) -> None:
    page.goto("https://the-internet.herokuapp.com/nested_frames")
    page.wait_for_load_state("domcontentloaded")

    page.wait_for_timeout(1000)

    all_frames = page.frames
    bottom_frame = None
    for frame in all_frames:
        try:
            content = frame.content()
            if "BOTTOM" in content:
                bottom_frame = frame
                break
        except Exception:
            continue

    assert bottom_frame is not None, (
        "BOTTOM text should be present in one of the nested frames"
    )
