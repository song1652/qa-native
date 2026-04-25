"""Fix login() to use wait_for_url instead of wait_for_load_state after submit.

This ensures we verify login success before proceeding, and catches session
invalidation earlier with a clear error.
"""
import re
from pathlib import Path

test_dir = Path("C:/TEST MANAGER/qa-native/tests/generated/directcloud")
files = sorted(test_dir.glob("tc_*.py"))

OLD_LOGIN_END = """\
    page.click("#new_btn_login")
    page.wait_for_load_state("networkidle", timeout=30000)"""

NEW_LOGIN_END = """\
    page.click("#new_btn_login")
    page.wait_for_load_state("networkidle", timeout=30000)
    page.wait_for_url(
        re.compile(r"/mybox|/recents|/sharedbox|/favorites|/trash"
                   r"|/mail|/notice|/contacts|/linkmanager|/filerequest|/aihome"),
        timeout=15000
    )"""

fixed = 0
skipped = 0

for fpath in files:
    content = fpath.read_text(encoding="utf-8")

    # Only fix files that have a login() helper function
    if "def login(page" not in content:
        skipped += 1
        continue
    if "wait_for_url" in content:
        skipped += 1
        continue
    if OLD_LOGIN_END not in content:
        skipped += 1
        continue

    new_content = content.replace(OLD_LOGIN_END, NEW_LOGIN_END, 1)

    # Ensure 're' is imported
    if "import re" not in new_content:
        new_content = new_content.replace("import json\n", "import json\nimport re\n", 1)

    fpath.write_text(new_content, encoding="utf-8")
    fixed += 1

print(f"Fixed: {fixed}, Skipped: {skipped}")
