import tempfile
import shutil
from pathlib import Path
from playwright.sync_api import Page, expect

BASE_URL = "https://the-internet.herokuapp.com/"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"


def test_file_upload(page: Page):
    """파일 업로드"""
    page.goto("https://the-internet.herokuapp.com/upload")
    page.wait_for_load_state("domcontentloaded")

    # 임시 텍스트 파일 생성
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".txt", prefix="test_upload", delete=False
    ) as f:
        f.write("test content")
        tmp_path = f.name

    # 파일명을 test_upload.txt로 맞추기 위해 rename
    target_path = Path(tmp_path).parent / "test_upload.txt"
    shutil.move(tmp_path, str(target_path))

    try:
        file_input = page.locator("#file-upload")
        expect(file_input).to_be_attached(timeout=10000)
        file_input.set_input_files(str(target_path))

        upload_button = page.locator("#file-submit")
        upload_button.click()

        page.wait_for_load_state("domcontentloaded")

        heading = page.locator("h3")
        expect(heading).to_contain_text("File Uploaded!", timeout=10000)

        uploaded_files = page.locator("#uploaded-files")
        expect(uploaded_files).to_contain_text("test_upload.txt", timeout=5000)
    finally:
        if target_path.exists():
            target_path.unlink()
