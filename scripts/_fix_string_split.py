"""Fix unterminated string literals caused by over-aggressive line breaking."""
import ast
import re
from pathlib import Path

test_dir = Path("C:/TEST MANAGER/qa-native/tests/generated/directcloud")

problem_files = [
    "tc_222_mail_send_button_mail_send_button.py",
    "tc_224_mybox_file_info_panel_mybox_file_info_panel.py",
    "tc_236_mybox_select_deselect_x_mybox_select_deselect_x.py",
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

    lines = fpath.read_text(encoding="utf-8").splitlines()
    new_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]
        # Detect broken string: line ends with a comma and the string wasn't closed
        # Pattern: line has odd number of unescaped quotes (unterminated)
        # Simple heuristic: if the line doesn't end the string it opens
        # Check if line has an open string by counting quotes
        stripped = line.rstrip()

        # Check if this line has an unterminated string
        # by trying to count quotes - if next line starts with whitespace
        # and continues a string, join them
        if (i + 1 < len(lines) and
                not stripped.endswith('"') and
                not stripped.endswith("'") and
                not stripped.endswith(",") and
                stripped.endswith(",") is False):
            # Check for continuation: next line is heavily indented
            next_line = lines[i + 1]
            next_stripped = next_line.lstrip()
            if (next_line.startswith("        ") and  # 8 spaces - extra indent from our split
                    not next_stripped.startswith("page.") and
                    not next_stripped.startswith("expect(") and
                    not next_stripped.startswith("login(") and
                    not next_stripped.startswith("def ") and
                    not next_stripped.startswith("#") and
                    not next_stripped.startswith("import ")):
                # This looks like a broken string - join
                new_lines.append(stripped + " " + next_stripped)
                i += 2
                continue

        # Also handle: line ends with comma inside string (no closing quote)
        # Count double quotes to detect unterminated string
        dq = stripped.count('"') - stripped.count('\\"')
        sq = stripped.count("'") - stripped.count("\\'")
        if (stripped.endswith(",") and (dq % 2 == 1) and
                i + 1 < len(lines)):
            next_line = lines[i + 1]
            next_stripped = next_line.lstrip()
            if next_line.startswith("        "):
                new_lines.append(stripped + " " + next_stripped)
                i += 2
                continue

        new_lines.append(line)
        i += 1

    content = "\n".join(new_lines) + "\n"
    fpath.write_text(content, encoding="utf-8")
    fixed += 1

print(f"Fixed {fixed} files")
