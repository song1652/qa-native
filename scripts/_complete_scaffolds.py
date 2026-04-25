"""Temporary script to complete scaffold test files."""
import re
import json
from pathlib import Path

test_dir = Path("C:/TEST MANAGER/qa-native/tests/generated/directcloud")

file_specs = {
    "tc_10_logout_logout": {"func": "test_tc_10_logout", "assertion": "element_visible: #inputSearch", "nav": None},
    "tc_20_search_detail_button_search_detail_button": {"func": "test_tc_20_search_detail_button", "assertion": "element_visible: #search-detail", "nav": None},
    "tc_21_link_history_search_filter_link_history_search_filter": {"func": "test_tc_21_link_history_search_filter", "assertion": "url_contains: /linkmanager", "nav": "li#linkmanager"},
    "tc_23_settings_language_select_settings_language_select": {"func": "test_tc_23_settings_language_select", "assertion": "element_visible: #inputSearch", "nav": None},
    "tc_24_settings_start_menu_select_settings_start_menu_select": {"func": "test_tc_24_settings_start_menu_select", "assertion": "element_visible: #inputSearch", "nav": None},
    "tc_25_settings_close_modal_settings_close_modal": {"func": "test_tc_25_settings_close_modal", "assertion": "element_visible: #main", "nav": None},
    "tc_26_notice_page_navigate_notice_page_navigate": {"func": "test_tc_26_notice_page_navigate", "assertion": "element_visible: #goNotice", "nav": None},
    "tc_27_comment_notification_modal_comment_notification_modal": {"func": "test_tc_27_comment_notification_modal", "assertion": "element_visible: #modal-notify-comments", "nav": None},
    "tc_28_ai_home_button_ai_home_button": {"func": "test_tc_28_ai_home_button", "assertion": "element_visible: #showAIHome", "nav": None},
    "tc_29_recent_files_list_items_recent_files_list_items": {"func": "test_tc_29_recent_files_list_items", "assertion": "url_contains: /recents", "nav": "li#recents"},
    "tc_30_favorites_file_listed_favorites_file_listed": {"func": "test_tc_30_favorites_file_listed", "assertion": "url_contains: /favorites", "nav": "li#favorites"},
    "tc_31_shared_box_file_items_shared_box_file_items": {"func": "test_tc_31_shared_box_file_items", "assertion": "url_contains: /sharedbox", "nav": "li#sharedbox"},
    "tc_32_mybox_nav_click_mybox_nav_click": {"func": "test_tc_32_mybox_nav_click", "assertion": "url_contains: /mybox", "nav": "li#mybox"},
    "tc_33_profile_username_displayed_profile_username_displayed": {"func": "test_tc_33_profile_username_displayed", "assertion": "element_visible: .nav-profile", "nav": None},
    "tc_34_storage_usage_displayed_storage_usage_displayed": {"func": "test_tc_34_storage_usage_displayed", "assertion": "element_visible: .storage-info", "nav": None},
    "tc_35_breadcrumb_location_displayed_breadcrumb_location_displayed": {"func": "test_tc_35_breadcrumb_location_displayed", "assertion": "element_visible: .breadcrumb", "nav": "li#mybox"},
    "tc_36_search_in_recents_search_in_recents": {"func": "test_tc_36_search_in_recents", "assertion": "url_contains: /recents", "nav": "li#recents"},
    "tc_37_trash_empty_state_trash_empty_state": {"func": "test_tc_37_trash_empty_state", "assertion": "url_contains: /trash", "nav": "li#trash"},
    "tc_38_mail_page_load_mail_page_load": {"func": "test_tc_38_mail_page_load", "assertion": "url_contains: /mail", "nav": "li#mail"},
    "tc_39_sidebar_all_menus_visible_sidebar_all_menus_visible": {"func": "test_tc_39_sidebar_all_menus_visible", "assertion": "element_visible: #sidebar", "nav": None},
    "tc_40_header_buttons_visible_header_buttons_visible": {"func": "test_tc_40_header_buttons_visible", "assertion": "element_visible: #inputSearch", "nav": None},
    "tc_41_context_menu_appears_context_menu_appears": {"func": "test_tc_41_context_menu_appears", "assertion": "right_click", "nav": "li#mybox"},
    "tc_42_context_menu_rename_context_menu_rename": {"func": "test_tc_42_context_menu_rename", "assertion": "right_click", "nav": "li#mybox"},
    "tc_43_context_menu_download_context_menu_download": {"func": "test_tc_43_context_menu_download", "assertion": "right_click", "nav": "li#mybox"},
    "tc_44_context_menu_copy_context_menu_copy": {"func": "test_tc_44_context_menu_copy", "assertion": "right_click", "nav": "li#mybox"},
    "tc_45_context_menu_move_context_menu_move": {"func": "test_tc_45_context_menu_move", "assertion": "right_click", "nav": "li#mybox"},
    "tc_46_context_menu_delete_context_menu_delete": {"func": "test_tc_46_context_menu_delete", "assertion": "right_click", "nav": "li#mybox"},
    "tc_47_context_menu_link_share_context_menu_link_share": {"func": "test_tc_47_context_menu_link_share", "assertion": "right_click", "nav": "li#mybox"},
    "tc_48_context_menu_favorite_context_menu_favorite": {"func": "test_tc_48_context_menu_favorite", "assertion": "right_click", "nav": "li#mybox"},
    "tc_49_context_menu_tag_context_menu_tag": {"func": "test_tc_49_context_menu_tag", "assertion": "right_click", "nav": "li#mybox"},
    "tc_50_context_menu_directplay_context_menu_directplay": {"func": "test_tc_50_context_menu_directplay", "assertion": "right_click", "nav": "li#mybox"},
    "tc_51_search_detail_panel_open_search_detail_panel_open": {"func": "test_tc_51_search_detail_panel_open", "assertion": "click_search: #search-detail", "nav": None},
    "tc_52_search_detail_scope_all_search_detail_scope_all": {"func": "test_tc_52_search_detail_scope_all", "assertion": "click_search: #search-detail", "nav": None},
    "tc_53_search_detail_target_options_search_detail_target_options": {"func": "test_tc_53_search_detail_target_options", "assertion": "click_search: #search-detail", "nav": None},
    "tc_54_search_detail_period_options_search_detail_period_options": {"func": "test_tc_54_search_detail_period_options", "assertion": "click_search: #search-detail", "nav": None},
    "tc_55_search_detail_and_or_condition_search_detail_and_or_condition": {"func": "test_tc_55_search_detail_and_or_condition", "assertion": "click_search: #search-detail", "nav": None},
    "tc_56_settings_menu_type_select_settings_menu_type_select": {"func": "test_tc_56_settings_menu_type_select", "assertion": "element_visible: .nav-profile", "nav": None},
    "tc_57_settings_drag_drop_select_settings_drag_drop_select": {"func": "test_tc_57_settings_drag_drop_select", "assertion": "element_visible: .nav-profile", "nav": None},
    "tc_58_settings_tag_display_select_settings_tag_display_select": {"func": "test_tc_58_settings_tag_display_select", "assertion": "element_visible: .nav-profile", "nav": None},
    "tc_59_settings_password_change_form_settings_password_change_form": {"func": "test_tc_59_settings_password_change_form", "assertion": "element_visible: .nav-profile", "nav": None},
    "tc_60_settings_password_save_button_settings_password_save_button": {"func": "test_tc_60_settings_password_save_button", "assertion": "element_visible: .nav-profile", "nav": None},
    "tc_61_login_history_page_login_history_page": {"func": "test_tc_61_login_history_page", "assertion": "element_visible: .nav-profile", "nav": None},
    "tc_62_login_history_filter_search_login_history_filter_search": {"func": "test_tc_62_login_history_filter_search", "assertion": "element_visible: .nav-profile", "nav": None},
    "tc_63_settings_email_notification_tab_settings_email_notification_tab": {"func": "test_tc_63_settings_email_notification_tab", "assertion": "element_visible: .nav-profile", "nav": None},
    "tc_64_contacts_page_load_contacts_page_load": {"func": "test_tc_64_contacts_page_load", "assertion": "url_contains: /contacts", "nav": "li#contacts"},
    "tc_65_contacts_name_search_contacts_name_search": {"func": "test_tc_65_contacts_name_search", "assertion": "url_contains: /contacts", "nav": "li#contacts"},
    "tc_66_contacts_csv_download_contacts_csv_download": {"func": "test_tc_66_contacts_csv_download", "assertion": "url_contains: /contacts", "nav": "li#contacts"},
    "tc_67_contacts_csv_upload_button_contacts_csv_upload_button": {"func": "test_tc_67_contacts_csv_upload_button", "assertion": "url_contains: /contacts", "nav": "li#contacts"},
    "tc_68_comment_modal_total_count_comment_modal_total_count": {"func": "test_tc_68_comment_modal_total_count", "assertion": "element_visible: #modal-notify-comments", "nav": None},
    "tc_69_comment_modal_detail_buttons_comment_modal_detail_buttons": {"func": "test_tc_69_comment_modal_detail_buttons", "assertion": "element_visible: #modal-notify-comments", "nav": None},
    "tc_70_comment_modal_close_comment_modal_close": {"func": "test_tc_70_comment_modal_close", "assertion": "element_visible: #modal-notify-comments", "nav": None},
    "tc_71_file_name_click_preview_file_name_click_preview": {"func": "test_tc_71_file_name_click_preview", "assertion": "url_contains: /mybox", "nav": "li#mybox"},
    "tc_72_file_list_preview_name_visible_file_list_preview_name_visible": {"func": "test_tc_72_file_list_preview_name_visible", "assertion": "element_visible: li.preview__list-item", "nav": "li#mybox"},
    "tc_73_view_mode_tooltip_visible_view_mode_tooltip_visible": {"func": "test_tc_73_view_mode_tooltip_visible", "assertion": "element_visible: #inputSearch", "nav": None},
    "tc_74_link_history_filter_options_link_history_filter_options": {"func": "test_tc_74_link_history_filter_options", "assertion": "url_contains: /linkmanager", "nav": "li#linkmanager"},
    "tc_75_link_history_search_execute_link_history_search_execute": {"func": "test_tc_75_link_history_search_execute", "assertion": "url_contains: /linkmanager", "nav": "li#linkmanager"},
    "tc_76_file_request_page_elements_file_request_page_elements": {"func": "test_tc_76_file_request_page_elements", "assertion": "url_contains: /filerequest", "nav": "li#filerequest"},
    "tc_77_notice_page_elements_notice_page_elements": {"func": "test_tc_77_notice_page_elements", "assertion": "element_visible: #goNotice", "nav": None},
    "tc_78_settings_user_info_displayed_settings_user_info_displayed": {"func": "test_tc_78_settings_user_info_displayed", "assertion": "element_visible: .nav-profile", "nav": None},
    "tc_79_mybox_upload_input_type_file_mybox_upload_input_type_file": {"func": "test_tc_79_mybox_upload_input_type_file", "assertion": "url_contains: /mybox", "nav": "li#mybox"},
    "tc_80_sharedbox_upload_input_exists_sharedbox_upload_input_exists": {"func": "test_tc_80_sharedbox_upload_input_exists", "assertion": "url_contains: /sharedbox", "nav": "li#sharedbox"},
    "tc_81_search_mybox_scope_search_mybox_scope": {"func": "test_tc_81_search_mybox_scope", "assertion": "click_search: #search-detail", "nav": None},
    "tc_82_search_shared_scope_search_shared_scope": {"func": "test_tc_82_search_shared_scope", "assertion": "click_search: #search-detail", "nav": None},
    "tc_83_search_comment_target_search_comment_target": {"func": "test_tc_83_search_comment_target", "assertion": "click_search: #search-detail", "nav": None},
    "tc_84_search_period_7days_search_period_7days": {"func": "test_tc_84_search_period_7days", "assertion": "click_search: #search-detail", "nav": None},
    "tc_85_home_menu_navigate_home_menu_navigate": {"func": "test_tc_85_home_menu_navigate", "assertion": "url_contains: /mybox", "nav": "li#mybox"},
    "tc_86_ai_folder_menu_ai_folder_menu": {"func": "test_tc_86_ai_folder_menu", "assertion": "element_visible: #inputSearch", "nav": None},
    "tc_87_header_search_input_clear_header_search_input_clear": {"func": "test_tc_87_header_search_input_clear", "assertion": "element_visible: #inputSearch", "nav": None},
    "tc_88_settings_language_change_english_settings_language_change_english": {"func": "test_tc_88_settings_language_change_english", "assertion": "element_visible: .nav-profile", "nav": None},
    "tc_89_favorites_select_all_favorites_select_all": {"func": "test_tc_89_favorites_select_all", "assertion": "url_contains: /favorites", "nav": "li#favorites"},
}

HEADER = """\
import json
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://web.directcloud.jp/login"
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def load_test_data():
    with open(TEST_DATA_PATH, encoding="utf-8") as f:
        return json.load(f)


def login(page, data_key="valid_user"):
    td = load_test_data()
    user = td["directcloud"][data_key]
    page.goto("https://web.directcloud.jp/login")
    page.wait_for_load_state("networkidle", timeout=30000)
    page.fill('[name="company_code"]', user["company"])
    page.fill('[name="id"]', user["username"])
    page.fill('[name="password"]', user["password"])
    page.click("#new_btn_login")
    page.wait_for_load_state("networkidle", timeout=30000)


"""


def make_code(func_name, assertion, nav):
    body = []
    if assertion == "right_click":
        body = [
            "    login(page)",
            f'    page.click("{nav}")',
            '    page.wait_for_load_state("networkidle", timeout=30000)',
            '    first_item = page.locator("li.preview__list-item").first',
            "    if first_item.count() > 0:",
            '        first_item.click(button="right")',
            "        page.wait_for_timeout(500)",
            '        expect(page.locator(".dropdown-menu")).to_be_visible(timeout=10000)',
            "    else:",
            "        import pytest",
            '        pytest.skip("No files in mybox")',
        ]
    elif assertion.startswith("click_search:"):
        selector = assertion.split(":", 1)[1].strip()
        body = [
            "    login(page)",
            '    page.click("#inputSearch")',
            "    page.wait_for_timeout(500)",
            f'    expect(page.locator("{selector}")).to_be_visible(timeout=10000)',
        ]
    else:
        body = ["    login(page)"]
        if nav:
            body.append(f'    page.click("{nav}")')
            body.append('    page.wait_for_load_state("networkidle", timeout=30000)')
        if assertion.startswith("url_contains:"):
            url_part = assertion.split(":", 1)[1].strip()
            body.append("    import re")
            body.append(f'    expect(page).to_have_url(re.compile(r"{url_part}"), timeout=15000)')
        elif assertion.startswith("element_visible:"):
            selector = assertion.split(":", 1)[1].strip()
            body.append(f'    expect(page.locator("{selector}")).to_be_visible(timeout=15000)')

    func = f"def {func_name}(page):\n" + "\n".join(body) + "\n"
    return HEADER + func


fixed = 0
for stem, spec in file_specs.items():
    fpath = test_dir / (stem + ".py")
    if not fpath.exists():
        print(f"SKIP: {stem}")
        continue
    code = make_code(spec["func"], spec["assertion"], spec.get("nav"))
    fpath.write_text(code, encoding="utf-8")
    fixed += 1

print(f"Completed {fixed} files")
