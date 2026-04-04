"""Playwright 테스트 — test_file_upload (tc_15)"""
import tempfile
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"


def test_file_upload(page):
    page.goto(BASE_URL + "upload")
    tmp_dir = Path(tempfile.mkdtemp())
    tmp_file = tmp_dir / "test_upload.txt"
    tmp_file.write_text("test content", encoding="utf-8")
    page.locator("#file-upload").set_input_files(str(tmp_file))
    page.locator("#file-submit").click()
    page.wait_for_load_state("domcontentloaded")
    expect(page.locator("h3")).to_contain_text("File Uploaded!", timeout=5000)
    expect(page.locator("#uploaded-files")).to_contain_text("test_upload.txt", timeout=5000)
