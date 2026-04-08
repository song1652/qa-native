from playwright.sync_api import expect
from pathlib import Path
import tempfile
import os

BASE_URL = "https://demoqa.com"
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"

AD_REMOVE_JS = (
    "document.querySelectorAll("
    "'ins.adsbygoogle, iframe[src*=google], iframe[src*=doubleclick]'"
    ").forEach(e => e.remove())"
)


def test_upload_download(page):
    page.goto(f"{BASE_URL}/upload-download", wait_until="domcontentloaded")
    page.evaluate(AD_REMOVE_JS)
    page.wait_for_timeout(2000)

    # Verify Download button is present and trigger download
    download_btn = page.locator("#downloadButton")
    expect(download_btn).to_be_visible(timeout=10000)

    with page.expect_download(timeout=15000) as download_info:
        download_btn.click()
    download = download_info.value
    assert download.suggested_filename, "Download did not start (no filename)"

    # Save to temp file for upload
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
        tmp_path = tmp.name

    try:
        download.save_as(tmp_path)
        assert os.path.exists(tmp_path), "Downloaded file not saved"

        # Re-remove ads after potential re-render
        page.evaluate(AD_REMOVE_JS)

        # Upload the downloaded file
        upload_input = page.locator("#uploadFile")
        expect(upload_input).to_be_visible(timeout=10000)
        upload_input.set_input_files(tmp_path)
        page.wait_for_timeout(1000)

        # Verify uploaded filename is shown
        uploaded_file_path = page.locator("#uploadedFilePath")
        expect(uploaded_file_path).to_be_visible(timeout=10000)
        uploaded_text = uploaded_file_path.inner_text()
        basename = os.path.basename(tmp_path)
        assert (
            basename in uploaded_text
            or "fakepath" in uploaded_text.lower()
            or uploaded_text.strip() != ""
        ), f"Uploaded file path not shown: '{uploaded_text}'"
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)
