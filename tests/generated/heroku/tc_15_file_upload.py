"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_15_file_upload (tc_15)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
import tempfile
from pathlib import Path

from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_file_upload(page):
    """파일 업로드"""
    page.goto(BASE_URL + "upload")

    # Create a temporary file to upload
    with tempfile.NamedTemporaryFile(
        suffix=".txt", prefix="test_upload_", delete=False, mode="w"
    ) as tmp:
        tmp.write("test upload content")
        tmp_path = tmp.name

    upload_file_name = Path(tmp_path).name

    # Set file on the file input
    page.locator("#file-upload").set_input_files(tmp_path)

    # Click upload button
    page.locator("#file-submit").click()

    # Verify upload success
    expect(page.locator("h3")).to_contain_text("File Uploaded!", timeout=10000)
    expect(page.locator("#uploaded-files")).to_contain_text(upload_file_name)
