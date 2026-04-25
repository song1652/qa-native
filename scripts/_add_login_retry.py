"""Add login retry logic to all generated test files to handle parallel session conflicts."""
import re
from pathlib import Path

test_dir = Path("C:/TEST MANAGER/qa-native/tests/generated/directcloud")
files = sorted(test_dir.glob("tc_*.py"))

OLD_LOGIN = """\
def login(page, data_key="valid_user"):
    td = load_test_data()
    user = td["directcloud"][data_key]
    page.goto("https://web.directcloud.jp/login")
    page.wait_for_load_state("networkidle", timeout=30000)
    page.fill('[name="company_code"]', user["company"])
    page.fill('[name="id"]', user["username"])
    page.fill('[name="password"]', user["password"])
    page.click("#new_btn_login")
    page.wait_for_load_state("networkidle", timeout=30000)"""

NEW_LOGIN = """\
def login(page, data_key="valid_user"):
    import re as _re
    td = load_test_data()
    user = td["directcloud"][data_key]
    _logged_in = _re.compile(
        r"/mybox|/recents|/sharedbox|/favorites|/trash"
        r"|/mail|/notice|/contacts|/linkmanager|/filerequest|/aihome"
    )
    for _attempt in range(3):
        page.goto("https://web.directcloud.jp/login")
        page.wait_for_load_state("networkidle", timeout=30000)
        page.fill('[name="company_code"]', user["company"])
        page.fill('[name="id"]', user["username"])
        page.fill('[name="password"]', user["password"])
        page.click("#new_btn_login")
        page.wait_for_load_state("networkidle", timeout=30000)
        if _logged_in.search(page.url):
            return
        if _attempt < 2:
            page.wait_for_timeout(3000)
    raise AssertionError(f"Login failed after 3 attempts. URL: {page.url}")"""

fixed = 0
already = 0
not_found = 0

for fpath in files:
    content = fpath.read_text(encoding="utf-8")
    if OLD_LOGIN in content:
        new_content = content.replace(OLD_LOGIN, NEW_LOGIN, 1)
        fpath.write_text(new_content, encoding="utf-8")
        fixed += 1
    elif "_attempt" in content:
        already += 1
    else:
        not_found += 1

print(f"Fixed: {fixed}, Already updated: {already}, No login(): {not_found}")
