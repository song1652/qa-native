"""Playwright 테스트 — test_upload_download (tc_100)"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://demoqa.com"
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"

import tempfile, os

def test_upload_download(page):
    """Upload and download"""
    page.goto(BASE_URL + "/upload-download")
    page.wait_for_load_state("domcontentloaded")

    # Upload a test file
    tmp = tempfile.NamedTemporaryFile(suffix=".txt", delete=False, prefix="upload_test_")
    tmp.write(b"test content")
    tmp.close()
    try:
        page.locator("#uploadFile").set_input_files(tmp.name)
        expect(page.locator("#uploadedFilePath")).to_be_visible(timeout=5000)
    finally:
        os.unlink(tmp.name)
