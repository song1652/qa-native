import pytest
from playwright.sync_api import expect
import json
import re
from pathlib import Path
import tempfile
import os

BASE_URL = "https://the-internet.herokuapp.com/"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"


def test_file_upload(page):
    file_path = "/tmp/test_upload.txt"
    with open(file_path, "w") as f:
        f.write("test content")

    try:
        page.goto(BASE_URL + "upload")
        page.locator("#file-upload").set_input_files(file_path)
        page.locator("#file-submit").click()
        expect(page.locator("h3")).to_contain_text("File Uploaded!", timeout=10000)
        expect(page.locator("#uploaded-files")).to_contain_text("test_upload.txt", timeout=10000)
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)
