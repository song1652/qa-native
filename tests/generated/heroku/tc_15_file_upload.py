"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: test_file_upload (tc_15)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
import tempfile
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"


def test_file_upload(page):
    """파일 업로드 — 임시 파일 생성 후 업로드, File Uploaded! 확인"""
    page.goto(BASE_URL + "upload")

    # 임시 파일 생성
    tmp_dir = Path(tempfile.mkdtemp())
    tmp_file = tmp_dir / "test_upload.txt"
    tmp_file.write_text("test content", encoding="utf-8")

    page.locator("#file-upload").set_input_files(str(tmp_file))
    page.locator("#file-submit").click()
    page.wait_for_load_state("domcontentloaded")

    expect(page.locator("h3")).to_contain_text("File Uploaded!", timeout=5000)
    expect(page.locator("#uploaded-files")).to_contain_text("test_upload.txt", timeout=5000)
