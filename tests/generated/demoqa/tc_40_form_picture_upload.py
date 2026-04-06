"""Playwright 테스트 — test_form_picture_upload (tc_40)"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://demoqa.com"
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"

import tempfile

def test_form_picture_upload(page):
    """Form picture upload"""
    page.goto(BASE_URL + "/automation-practice-form")
    page.wait_for_load_state("domcontentloaded")

    import os
    tmp = tempfile.NamedTemporaryFile(suffix=".txt", delete=False, prefix="test_image_")
    tmp.write(b"test content")
    tmp.close()
    try:
        page.locator("#uploadPicture").set_input_files(tmp.name)
        val = page.locator("#uploadPicture").evaluate("el => el.files[0]?.name")
        assert val, "File should be uploaded"
    finally:
        os.unlink(tmp.name)
