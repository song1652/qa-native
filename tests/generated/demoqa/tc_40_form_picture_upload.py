import tempfile
import os
from playwright.sync_api import Page

BASE_URL = "https://demoqa.com"

AD_REMOVE_JS = (
    "document.querySelectorAll("
    "'ins.adsbygoogle, iframe[src*=google], iframe[src*=doubleclick], #fixedban, footer'"
    ").forEach(e => e.remove())"
)


def test_form_picture_upload(page: Page):
    page.goto(f"{BASE_URL}/automation-practice-form")
    page.wait_for_load_state("domcontentloaded")
    page.wait_for_timeout(2000)

    page.evaluate(AD_REMOVE_JS)

    # Create a temporary file to upload
    with tempfile.NamedTemporaryFile(suffix=".txt", prefix="test_image", delete=False) as tmp:
        tmp.write(b"test file content")
        tmp_path = tmp.name

    try:
        upload_input = page.locator("#uploadPicture")
        upload_input.set_input_files(tmp_path)
        page.wait_for_timeout(500)

        # Verify file name is shown in the input value
        uploaded_filename = os.path.basename(tmp_path)
        upload_value = upload_input.evaluate("el => el.value")
        assert uploaded_filename in upload_value, (
            f"Expected '{uploaded_filename}' in upload field value, got '{upload_value}'"
        )
    finally:
        os.unlink(tmp_path)
