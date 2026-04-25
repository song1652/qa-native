"""Fix E701 (one-liner with) and E501 (long locator strings) in generated test files."""
import re
from pathlib import Path

test_dir = Path("C:/TEST MANAGER/qa-native/tests/generated/directcloud")

problem_files = [
    "tc_252_search_clear_button_search_clear_button.py",
    "tc_260_mybox_link_create_with_password_mybox_link_create_with_password.py",
    "tc_261_mybox_link_create_with_expiry_mybox_link_create_with_expiry.py",
    "tc_262_mybox_link_create_download_limit_mybox_link_create_download_limit.py",
    "tc_271_mybox_file_select_count_display_mybox_file_select_count_display.py",
    "tc_277_mybox_preview_modal_close_mybox_preview_modal_close.py",
    "tc_278_mybox_preview_modal_download_mybox_preview_modal_download.py",
    "tc_296_mybox_right_panel_file_tags_mybox_right_panel_file_tags.py",
]

fixed = 0

for fname in problem_files:
    fpath = test_dir / fname
    if not fpath.exists():
        continue

    content = fpath.read_text(encoding="utf-8")
    original = content

    # Fix E701: "with open(...) as f: return json.load(f)" -> split to two lines
    content = re.sub(
        r'(\s+)(with open\(TEST_DATA_PATH, encoding="utf-8"\) as f): return json\.load\(f\)',
        r'\1\2:\n\1    return json.load(f)',
        content
    )

    # Fix E501: long locator strings - wrap in parentheses with line break
    lines = content.splitlines()
    new_lines = []
    for line in lines:
        if len(line) > 120 and 'page.locator(' in line and '"' in line:
            # Find the locator call and split at a reasonable point
            # Wrap the long string with parentheses using a selector variable
            indent = len(line) - len(line.lstrip())
            ind = " " * indent
            # Try to find a comma in the middle of the string to break at
            # Strategy: find the locator string content and truncate to 120
            # Simple fix: find a comma after char 80 and break there
            m = re.search(r'(page\.locator\()(")(.*?)(")\)', line)
            if m and len(line) > 120:
                prefix = line[:m.start()]
                suffix = line[m.end():]
                selector = m.group(3)
                # Find best break point (comma) between char 60-90 of selector
                break_candidates = [i for i, c in enumerate(selector) if c == ',']
                best = None
                for b in break_candidates:
                    if 60 <= b <= 100:
                        best = b
                        break
                if best is not None:
                    sel1 = selector[:best + 1].strip()
                    sel2 = selector[best + 1:].strip()
                    var_indent = ind
                    new_lines.append(f'{var_indent}sel = (')
                    new_lines.append(f'{var_indent}    "{sel1}"')
                    new_lines.append(f'{var_indent}    " {sel2}"')
                    new_lines.append(f'{var_indent})')
                    new_lines.append(f'{var_indent}page.locator(sel){suffix}')
                    continue
        new_lines.append(line)

    content = "\n".join(new_lines) + "\n"

    if content != original:
        fpath.write_text(content, encoding="utf-8")
        fixed += 1
        print(f"Fixed: {fname}")

print(f"\nTotal fixed: {fixed}")
