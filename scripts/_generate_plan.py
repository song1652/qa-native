#!/usr/bin/env python3
"""Generate plan for all 120 test cases and update pipeline.json."""
import json
import os

PIPELINE = os.path.join(os.path.dirname(__file__), '..', 'state', 'pipeline.json')
BASE = "https://the-internet.herokuapp.com"


def make_plan():
    """Return dict of plan entries keyed by tc_id."""
    plans = {}

    # ── tc_01: Login success ──
    plans["tc_01"] = {
        "case_name": "tc_01_login_success",
        "case_type": "structured",
        "description": "Verify successful login with valid credentials",
        "steps": [
            {"action": "goto", "selector": "", "value": f"{BASE}/login"},
            {"action": "fill", "selector": "#username", "value": "{{valid_user.username}}"},
            {"action": "fill", "selector": "#password", "value": "{{valid_user.password}}"},
            {"action": "click", "selector": "button.radius", "value": ""},
        ],
        "assertion": {"type": "url", "expected": "/secure"},
    }

    # ── tc_02: Login failure ──
    plans["tc_02"] = {
        "case_name": "tc_02_login_invalid_user",
        "case_type": "structured",
        "description": "Verify login fails with invalid credentials",
        "steps": [
            {"action": "goto", "selector": "", "value": f"{BASE}/login"},
            {"action": "fill", "selector": "#username", "value": "{{invalid_user.username}}"},
            {"action": "fill", "selector": "#password", "value": "{{invalid_user.password}}"},
            {"action": "click", "selector": "button.radius", "value": ""},
        ],
        "assertion": {"type": "text", "expected": "Your username is invalid!"},
    }

    # ── tc_03: Login then logout ──
    plans["tc_03"] = {
        "case_name": "tc_03_login_then_logout",
        "case_type": "structured",
        "description": "Verify login then logout redirects back to login page",
        "steps": [
            {"action": "goto", "selector": "", "value": f"{BASE}/login"},
            {"action": "fill", "selector": "#username", "value": "{{valid_user.username}}"},
            {"action": "fill", "selector": "#password", "value": "{{valid_user.password}}"},
            {"action": "click", "selector": "button.radius", "value": ""},
            {"action": "click", "selector": "a[href='/logout']", "value": ""},
        ],
        "assertion": {"type": "text", "expected": "You logged out of the secure area!"},
    }

    # ── tc_04: Checkbox toggle ──
    plans["tc_04"] = {
        "case_name": "tc_04_checkbox_toggle",
        "case_type": "structured",
        "description": "Toggle both checkboxes and verify states",
        "steps": [
            {"action": "goto", "selector": "", "value": f"{BASE}/checkboxes"},
            {"action": "click", "selector": "#checkboxes input:nth-of-type(1)", "value": ""},
            {"action": "click", "selector": "#checkboxes input:nth-of-type(2)", "value": ""},
        ],
        "assertion": {"type": "attribute", "expected": "checkbox1=checked,checkbox2=unchecked"},
    }

    # ── tc_05: Dropdown select ──
    plans["tc_05"] = {
        "case_name": "tc_05_dropdown_select_option",
        "case_type": "structured",
        "description": "Select options from dropdown and verify values",
        "steps": [
            {"action": "goto", "selector": "", "value": f"{BASE}/dropdown"},
            {"action": "select", "selector": "#dropdown", "value": "1"},
            {"action": "select", "selector": "#dropdown", "value": "2"},
        ],
        "assertion": {"type": "attribute", "expected": "value=2"},
    }

    # ── tc_06: Add/remove elements ──
    plans["tc_06"] = {
        "case_name": "tc_06_add_remove_elements",
        "case_type": "structured",
        "description": "Add 3 elements, verify count, delete 1, verify count",
        "steps": [
            {"action": "goto", "selector": "", "value": f"{BASE}/add_remove_elements/"},
            {"action": "click", "selector": "button[onclick='addElement()']", "value": ""},
            {"action": "click", "selector": "button[onclick='addElement()']", "value": ""},
            {"action": "click", "selector": "button[onclick='addElement()']", "value": ""},
            {"action": "click", "selector": "#elements .added-manually:first-child", "value": ""},
        ],
        "assertion": {"type": "visible", "expected": "2 delete buttons remaining"},
    }

    # ── tc_07: JS Alert ──
    plans["tc_07"] = {
        "case_name": "tc_07_js_alert",
        "case_type": "structured",
        "description": "Click JS Alert button and accept the alert dialog",
        "steps": [
            {"action": "goto", "selector": "", "value": f"{BASE}/javascript_alerts"},
            {"action": "click", "selector": "button[onclick='jsAlert()']", "value": ""},
        ],
        "assertion": {"type": "text", "expected": "You successfully clicked an alert"},
    }

    # ── tc_08: JS Confirm accept ──
    plans["tc_08"] = {
        "case_name": "tc_08_js_confirm_accept",
        "case_type": "structured",
        "description": "Click JS Confirm and accept the dialog",
        "steps": [
            {"action": "goto", "selector": "", "value": f"{BASE}/javascript_alerts"},
            {"action": "click", "selector": "button[onclick='jsConfirm()']", "value": ""},
        ],
        "assertion": {"type": "text", "expected": "You clicked: Ok"},
    }

    # ── tc_09: JS Confirm dismiss ──
    plans["tc_09"] = {
        "case_name": "tc_09_js_confirm_dismiss",
        "case_type": "structured",
        "description": "Click JS Confirm and dismiss the dialog",
        "steps": [
            {"action": "goto", "selector": "", "value": f"{BASE}/javascript_alerts"},
            {"action": "click", "selector": "button[onclick='jsConfirm()']", "value": "dialog:dismiss"},
        ],
        "assertion": {"type": "text", "expected": "You clicked: Cancel"},
    }

    # ── tc_10: JS Prompt input ──
    plans["tc_10"] = {
        "case_name": "tc_10_js_prompt_input",
        "case_type": "structured",
        "description": "Click JS Prompt, enter text, and verify result",
        "steps": [
            {"action": "goto", "selector": "", "value": f"{BASE}/javascript_alerts"},
            {"action": "click", "selector": "button[onclick='jsPrompt()']", "value": "dialog:{{js_prompt.text}}"},
        ],
        "assertion": {"type": "text", "expected": "You entered: Hello Playwright"},
    }

    # ── tc_11: Hover user info ──
    plans["tc_11"] = {
        "case_name": "tc_11_hover_user_info",
        "case_type": "structured",
        "description": "Hover over user avatar and verify profile info appears",
        "steps": [
            {"action": "goto", "selector": "", "value": f"{BASE}/hovers"},
            {"action": "hover", "selector": ".figure:nth-child(3)", "value": ""},
        ],
        "assertion": {"type": "visible", "expected": "name: user1"},
    }

    # ── tc_12: Dynamic Controls checkbox remove/add ──
    plans["tc_12"] = {
        "case_name": "tc_12_dynamic_controls_checkbox_remove_add",
        "case_type": "structured",
        "description": "Remove checkbox, verify gone, add back, verify present",
        "steps": [
            {"action": "goto", "selector": "", "value": f"{BASE}/dynamic_controls"},
            {"action": "click", "selector": "#checkbox-example button", "value": ""},
            {"action": "wait", "selector": "#message", "value": ""},
            {"action": "click", "selector": "#checkbox-example button", "value": ""},
            {"action": "wait", "selector": "#checkbox", "value": ""},
        ],
        "assertion": {"type": "visible", "expected": "checkbox restored"},
    }

    # ── tc_13: Dynamic Controls enable input ──
    plans["tc_13"] = {
        "case_name": "tc_13_dynamic_controls_input_enable",
        "case_type": "structured",
        "description": "Enable the text input field and verify it becomes editable",
        "steps": [
            {"action": "goto", "selector": "", "value": f"{BASE}/dynamic_controls"},
            {"action": "click", "selector": "#input-example button", "value": ""},
            {"action": "wait", "selector": "#message", "value": ""},
        ],
        "assertion": {"type": "attribute", "expected": "input enabled"},
    }

    # ── tc_14: Key press detection ──
    plans["tc_14"] = {
        "case_name": "tc_14_key_press_detection",
        "case_type": "structured",
        "description": "Press a key and verify detection message",
        "steps": [
            {"action": "goto", "selector": "", "value": f"{BASE}/key_presses"},
            {"action": "click", "selector": "#target", "value": ""},
            {"action": "press", "selector": "#target", "value": "A"},
        ],
        "assertion": {"type": "text", "expected": "You entered: A"},
    }

    # ── tc_15: File upload ──
    plans["tc_15"] = {
        "case_name": "tc_15_file_upload",
        "case_type": "structured",
        "description": "Upload a file and verify upload success",
        "steps": [
            {"action": "goto", "selector": "", "value": f"{BASE}/upload"},
            {"action": "upload", "selector": "#file-upload", "value": "test_upload.txt"},
            {"action": "click", "selector": "#file-submit", "value": ""},
        ],
        "assertion": {"type": "text", "expected": "File Uploaded!"},
    }

    # ── tc_16: Slider manipulation ──
    plans["tc_16"] = {
        "case_name": "tc_16_horizontal_slider",
        "case_type": "structured",
        "description": "Move horizontal slider and verify value changes",
        "steps": [
            {"action": "goto", "selector": "", "value": f"{BASE}/horizontal_slider"},
            {"action": "fill", "selector": "input[type='range']", "value": "3.5"},
        ],
        "assertion": {"type": "text", "expected": "3.5"},
    }

    # ── tc_17: Sortable data table ──
    plans["tc_17"] = {
        "case_name": "tc_17_sortable_data_table",
        "case_type": "structured",
        "description": "Click table header to sort and verify order",
        "steps": [
            {"action": "goto", "selector": "", "value": f"{BASE}/tables"},
            {"action": "click", "selector": "#table1 thead tr th:nth-child(1)", "value": ""},
        ],
        "assertion": {"type": "text", "expected": "sorted ascending by Last Name"},
    }

    # ── tc_18: Dynamic loading wait ──
    plans["tc_18"] = {
        "case_name": "tc_18_dynamic_loading_wait",
        "case_type": "structured",
        "description": "Click Start and wait for hidden element to appear",
        "steps": [
            {"action": "goto", "selector": "", "value": f"{BASE}/dynamic_loading/1"},
            {"action": "click", "selector": "#start button", "value": ""},
            {"action": "wait", "selector": "#finish", "value": ""},
        ],
        "assertion": {"type": "text", "expected": "Hello World!"},
    }

    # ── tc_19: Forgot password email submit ──
    plans["tc_19"] = {
        "case_name": "tc_19_forgot_password_submit",
        "case_type": "structured",
        "description": "Submit email on forgot password page",
        "steps": [
            {"action": "goto", "selector": "", "value": f"{BASE}/forgot_password"},
            {"action": "fill", "selector": "#email", "value": "{{forgot_email.email}}"},
            {"action": "click", "selector": "#form_submit", "value": ""},
        ],
        "assertion": {"type": "text", "expected": "Your e-mail's been sent!"},
    }

    # ── tc_20: Number input ──
    plans["tc_20"] = {
        "case_name": "tc_20_number_input",
        "case_type": "structured",
        "description": "Enter a number in the input field and verify",
        "steps": [
            {"action": "goto", "selector": "", "value": f"{BASE}/inputs"},
            {"action": "fill", "selector": "input[type='number']", "value": "42"},
        ],
        "assertion": {"type": "attribute", "expected": "value=42"},
    }

    # ── tc_21: A/B Test page load ──
    plans["tc_21"] = {
        "case_name": "tc_21_ab_test_page_load",
        "case_type": "structured",
        "description": "Verify A/B test page loads successfully",
        "steps": [
            {"action": "goto", "selector": "", "value": f"{BASE}/abtest"},
        ],
        "assertion": {"type": "visible", "expected": "h3 heading present (A/B Test or No A/B Test)"},
    }

    # ── tc_22: A/B Test content variation ──
    plans["tc_22"] = {
        "case_name": "tc_22_ab_test_content_variation",
        "case_type": "structured",
        "description": "Verify A/B test page shows content variation",
        "steps": [
            {"action": "goto", "selector": "", "value": f"{BASE}/abtest"},
        ],
        "assertion": {"type": "text", "expected": "Also, A/B"},
    }

    # ── tc_23: Basic Auth success ──
    plans["tc_23"] = {
        "case_name": "tc_23_basic_auth_success",
        "case_type": "structured",
        "description": "Access Basic Auth page with credentials in URL",
        "steps": [
            {"action": "goto", "selector": "", "value": "https://admin:admin@the-internet.herokuapp.com/basic_auth"},
        ],
        "assertion": {"type": "text", "expected": "Congratulations!"},
    }

    # ── tc_24: Broken images detection ──
    plans["tc_24"] = {
        "case_name": "tc_24_broken_images_detect",
        "case_type": "structured",
        "description": "Detect broken images on the page",
        "steps": [
            {"action": "goto", "selector": "", "value": f"{BASE}/broken_images"},
            {"action": "evaluate", "selector": "", "value": "check img naturalWidth"},
        ],
        "assertion": {"type": "visible", "expected": "broken images detected"},
    }

    # ── tc_25: Valid images load ──
    plans["tc_25"] = {
        "case_name": "tc_25_valid_images_load",
        "case_type": "structured",
        "description": "Verify at least one image loads correctly",
        "steps": [
            {"action": "goto", "selector": "", "value": f"{BASE}/broken_images"},
            {"action": "evaluate", "selector": "", "value": "check img naturalWidth > 0"},
        ],
        "assertion": {"type": "visible", "expected": "at least one valid image"},
    }

    # ── tc_26: Challenging DOM table data ──
    plans["tc_26"] = {
        "case_name": "tc_26_challenging_dom_table_read",
        "case_type": "structured",
        "description": "Read data from the Challenging DOM table",
        "steps": [
            {"action": "goto", "selector": "", "value": f"{BASE}/challenging_dom"},
        ],
        "assertion": {"type": "visible", "expected": "table with data rows"},
    }

    # ── tc_27: Challenging DOM button click ──
    plans["tc_27"] = {
        "case_name": "tc_27_challenging_dom_button_click",
        "case_type": "structured",
        "description": "Click one of the challenging DOM buttons",
        "steps": [
            {"action": "goto", "selector": "", "value": f"{BASE}/challenging_dom"},
            {"action": "click", "selector": ".large-2.columns a.button", "value": ""},
        ],
        "assertion": {"type": "visible", "expected": "button clicked, page reloaded"},
    }

    # ── tc_28: Challenging DOM canvas ──
    plans["tc_28"] = {
        "case_name": "tc_28_challenging_dom_canvas",
        "case_type": "structured",
        "description": "Verify canvas element exists on Challenging DOM page",
        "steps": [
            {"action": "goto", "selector": "", "value": f"{BASE}/challenging_dom"},
        ],
        "assertion": {"type": "visible", "expected": "canvas#canvas"},
    }

    # ── tc_29: Context menu right-click alert ──
    plans["tc_29"] = {
        "case_name": "tc_29_context_menu_alert",
        "case_type": "structured",
        "description": "Right-click on the box to trigger context menu alert",
        "steps": [
            {"action": "goto", "selector": "", "value": f"{BASE}/context_menu"},
            {"action": "click", "selector": "#hot-spot", "value": "right-click"},
        ],
        "assertion": {"type": "text", "expected": "You selected a context menu"},
    }

    # ── tc_30: Context menu page content ──
    plans["tc_30"] = {
        "case_name": "tc_30_context_menu_content",
        "case_type": "structured",
        "description": "Verify context menu page content elements exist",
        "steps": [
            {"action": "goto", "selector": "", "value": f"{BASE}/context_menu"},
        ],
        "assertion": {"type": "visible", "expected": "#hot-spot element visible"},
    }

    # ── tc_31: Disappearing elements exist ──
    plans["tc_31"] = {
        "case_name": "tc_31_disappearing_elements_exist",
        "case_type": "structured",
        "description": "Verify navigation elements are present on the page",
        "steps": [
            {"action": "goto", "selector": "", "value": f"{BASE}/disappearing_elements"},
        ],
        "assertion": {"type": "visible", "expected": "navigation buttons visible"},
    }

    # ── tc_32: Disappearing elements refresh change ──
    plans["tc_32"] = {
        "case_name": "tc_32_disappearing_elements_refresh",
        "case_type": "structured",
        "description": "Refresh page and verify element count may change",
        "steps": [
            {"action": "goto", "selector": "", "value": f"{BASE}/disappearing_elements"},
            {"action": "evaluate", "selector": "", "value": "count nav li elements"},
            {"action": "goto", "selector": "", "value": f"{BASE}/disappearing_elements"},
        ],
        "assertion": {"type": "visible", "expected": "element count may differ after refresh"},
    }

    # ── tc_33: Drag and drop A to B ──
    plans["tc_33"] = {
        "case_name": "tc_33_drag_drop_a_to_b",
        "case_type": "structured",
        "description": "Drag column A to column B position",
        "steps": [
            {"action": "goto", "selector": "", "value": f"{BASE}/drag_and_drop"},
            {"action": "drag", "selector": "#column-a", "value": "#column-b"},
        ],
        "assertion": {"type": "text", "expected": "column-a header becomes B"},
    }

    # ── tc_34: Drag and drop B to A ──
    plans["tc_34"] = {
        "case_name": "tc_34_drag_drop_b_to_a",
        "case_type": "structured",
        "description": "Drag column B to column A position",
        "steps": [
            {"action": "goto", "selector": "", "value": f"{BASE}/drag_and_drop"},
            {"action": "drag", "selector": "#column-b", "value": "#column-a"},
        ],
        "assertion": {"type": "text", "expected": "column-b header becomes A"},
    }

    # ── tc_35: Dynamic content load ──
    plans["tc_35"] = {
        "case_name": "tc_35_dynamic_content_load",
        "case_type": "structured",
        "description": "Verify dynamic content rows load on the page",
        "steps": [
            {"action": "goto", "selector": "", "value": f"{BASE}/dynamic_content"},
        ],
        "assertion": {"type": "visible", "expected": "content rows with images and text"},
    }

    # ── tc_36: Dynamic content refresh change ──
    plans["tc_36"] = {
        "case_name": "tc_36_dynamic_content_refresh",
        "case_type": "structured",
        "description": "Refresh and verify content changes",
        "steps": [
            {"action": "goto", "selector": "", "value": f"{BASE}/dynamic_content"},
            {"action": "evaluate", "selector": "", "value": "capture row text"},
            {"action": "goto", "selector": "", "value": f"{BASE}/dynamic_content"},
        ],
        "assertion": {"type": "text", "expected": "content text differs after refresh"},
    }

    # ── tc_37: Entry Ad modal display ──
    plans["tc_37"] = {
        "case_name": "tc_37_entry_ad_modal_display",
        "case_type": "structured",
        "description": "Verify Entry Ad modal appears on page load",
        "steps": [
            {"action": "goto", "selector": "", "value": f"{BASE}/entry_ad"},
            {"action": "wait", "selector": ".modal", "value": ""},
        ],
        "assertion": {"type": "visible", "expected": "modal dialog visible"},
    }

    # ── tc_38: Entry Ad modal close ──
    plans["tc_38"] = {
        "case_name": "tc_38_entry_ad_modal_close",
        "case_type": "structured",
        "description": "Close the Entry Ad modal",
        "steps": [
            {"action": "goto", "selector": "", "value": f"{BASE}/entry_ad"},
            {"action": "wait", "selector": ".modal", "value": ""},
            {"action": "click", "selector": ".modal-footer p", "value": ""},
        ],
        "assertion": {"type": "hidden", "expected": "modal dialog hidden after close"},
    }

    # ── tc_39: Exit Intent modal ──
    plans["tc_39"] = {
        "case_name": "tc_39_exit_intent_modal",
        "case_type": "structured",
        "description": "Trigger exit intent by moving mouse out of viewport",
        "steps": [
            {"action": "goto", "selector": "", "value": f"{BASE}/exit_intent"},
            {"action": "evaluate", "selector": "", "value": "dispatch mouseout event to document"},
        ],
        "assertion": {"type": "visible", "expected": "modal dialog displayed"},
    }

    # ── tc_40: File download links ──
    plans["tc_40"] = {
        "case_name": "tc_40_file_download_links",
        "case_type": "structured",
        "description": "Verify download links exist on the page",
        "steps": [
            {"action": "goto", "selector": "", "value": f"{BASE}/download"},
        ],
        "assertion": {"type": "visible", "expected": "download links present"},
    }

    # ── tc_41: File download execute ──
    plans["tc_41"] = {
        "case_name": "tc_41_file_download_execute",
        "case_type": "structured",
        "description": "Click a download link and verify file downloads",
        "steps": [
            {"action": "goto", "selector": "", "value": f"{BASE}/download"},
            {"action": "click", "selector": ".example a:first-child", "value": "download"},
        ],
        "assertion": {"type": "visible", "expected": "file downloaded successfully"},
    }

    # ── tc_42: Floating menu display ──
    plans["tc_42"] = {
        "case_name": "tc_42_floating_menu_display",
        "case_type": "structured",
        "description": "Verify floating menu is visible on page",
        "steps": [
            {"action": "goto", "selector": "", "value": f"{BASE}/floating_menu"},
        ],
        "assertion": {"type": "visible", "expected": "#menu visible"},
    }

    # ── tc_43: Floating menu fixed after scroll ──
    plans["tc_43"] = {
        "case_name": "tc_43_floating_menu_scroll_fixed",
        "case_type": "structured",
        "description": "Scroll down and verify floating menu stays visible",
        "steps": [
            {"action": "goto", "selector": "", "value": f"{BASE}/floating_menu"},
            {"action": "evaluate", "selector": "", "value": "window.scrollBy(0, 1000)"},
        ],
        "assertion": {"type": "visible", "expected": "#menu still visible after scroll"},
    }

    # ── tc_44: iFrame content access ──
    plans["tc_44"] = {
        "case_name": "tc_44_iframe_content_access",
        "case_type": "structured",
        "description": "Access iFrame and verify content inside",
        "steps": [
            {"action": "goto", "selector": "", "value": f"{BASE}/frames"},
            {"action": "click", "selector": "a[href='/iframe']", "value": ""},
        ],
        "assertion": {"type": "visible", "expected": "iFrame with TinyMCE editor"},
    }

    # ── tc_45: Frames page link list ──
    plans["tc_45"] = {
        "case_name": "tc_45_frames_link_list",
        "case_type": "structured",
        "description": "Verify links to Nested Frames and iFrame exist",
        "steps": [
            {"action": "goto", "selector": "", "value": f"{BASE}/frames"},
        ],
        "assertion": {"type": "visible", "expected": "Nested Frames and iFrame links"},
    }

    # ── tc_46: Nested Frames link navigation ──
    plans["tc_46"] = {
        "case_name": "tc_46_nested_frames_navigation",
        "case_type": "structured",
        "description": "Navigate to nested frames page from frames page",
        "steps": [
            {"action": "goto", "selector": "", "value": f"{BASE}/frames"},
            {"action": "click", "selector": "a[href='/nested_frames']", "value": ""},
        ],
        "assertion": {"type": "url", "expected": "/nested_frames"},
    }

    # ── tc_47: Nested frames parent frame ──
    plans["tc_47"] = {
        "case_name": "tc_47_nested_frames_parent",
        "case_type": "structured",
        "description": "Verify parent frame exists in nested frames",
        "steps": [
            {"action": "goto", "selector": "", "value": f"{BASE}/nested_frames"},
        ],
        "assertion": {"type": "visible", "expected": "frame-top frameset present"},
    }

    # ── tc_48: Nested frames bottom text ──
    plans["tc_48"] = {
        "case_name": "tc_48_nested_frames_bottom_text",
        "case_type": "structured",
        "description": "Verify bottom frame contains expected text",
        "steps": [
            {"action": "goto", "selector": "", "value": f"{BASE}/nested_frames"},
        ],
        "assertion": {"type": "text", "expected": "BOTTOM"},
    }

    # ── tc_49: Geolocation button click ──
    plans["tc_49"] = {
        "case_name": "tc_49_geolocation_button_click",
        "case_type": "structured",
        "description": "Click Where am I button and verify response",
        "steps": [
            {"action": "goto", "selector": "", "value": f"{BASE}/geolocation"},
            {"action": "click", "selector": "button[onclick='getLocation()']", "value": ""},
        ],
        "assertion": {"type": "visible", "expected": "latitude and longitude displayed"},
    }

    # ── tc_50: Infinite scroll initial content ──
    plans["tc_50"] = {
        "case_name": "tc_50_infinite_scroll_initial",
        "case_type": "structured",
        "description": "Verify initial content loads on infinite scroll page",
        "steps": [
            {"action": "goto", "selector": "", "value": f"{BASE}/infinite_scroll"},
        ],
        "assertion": {"type": "visible", "expected": ".jscroll-inner content visible"},
    }

    # ── tc_51: Infinite scroll load more ──
    plans["tc_51"] = {
        "case_name": "tc_51_infinite_scroll_load_more",
        "case_type": "structured",
        "description": "Scroll down to trigger loading of additional content",
        "steps": [
            {"action": "goto", "selector": "", "value": f"{BASE}/infinite_scroll"},
            {"action": "evaluate", "selector": "", "value": "window.scrollTo(0, document.body.scrollHeight)"},
            {"action": "wait", "selector": ".jscroll-added", "value": ""},
        ],
        "assertion": {"type": "visible", "expected": "additional content paragraphs loaded"},
    }

    # ── tc_52: jQuery UI menu items ──
    plans["tc_52"] = {
        "case_name": "tc_52_jquery_ui_menu_items",
        "case_type": "structured",
        "description": "Verify jQuery UI menu items are displayed",
        "steps": [
            {"action": "goto", "selector": "", "value": f"{BASE}/jqueryui/menu"},
        ],
        "assertion": {"type": "visible", "expected": "menu items visible"},
    }

    # ── tc_53: jQuery UI submenu hover ──
    plans["tc_53"] = {
        "case_name": "tc_53_jquery_ui_submenu_hover",
        "case_type": "structured",
        "description": "Hover on menu item to show submenu",
        "steps": [
            {"action": "goto", "selector": "", "value": f"{BASE}/jqueryui/menu"},
            {"action": "hover", "selector": "#ui-id-3", "value": ""},
        ],
        "assertion": {"type": "visible", "expected": "submenu items displayed"},
    }

    # ── tc_54: jQuery UI menu click ──
    plans["tc_54"] = {
        "case_name": "tc_54_jquery_ui_menu_click",
        "case_type": "structured",
        "description": "Click a menu item and verify action",
        "steps": [
            {"action": "goto", "selector": "", "value": f"{BASE}/jqueryui/menu"},
            {"action": "hover", "selector": "#ui-id-3", "value": ""},
            {"action": "click", "selector": "#ui-id-4", "value": ""},
        ],
        "assertion": {"type": "visible", "expected": "menu action executed"},
    }

    # ── tc_55: JavaScript error console ──
    plans["tc_55"] = {
        "case_name": "tc_55_js_error_console",
        "case_type": "structured",
        "description": "Verify console error exists on JavaScript error page",
        "steps": [
            {"action": "goto", "selector": "", "value": f"{BASE}/javascript_error"},
        ],
        "assertion": {"type": "console", "expected": "Cannot read properties of undefined"},
    }

    # ── tc_56: Large DOM page load ──
    plans["tc_56"] = {
        "case_name": "tc_56_large_dom_page_load",
        "case_type": "structured",
        "description": "Verify large DOM page loads completely",
        "steps": [
            {"action": "goto", "selector": "", "value": f"{BASE}/large"},
        ],
        "assertion": {"type": "visible", "expected": "page with large DOM loaded"},
    }

    # ── tc_57: Large DOM specific element ──
    plans["tc_57"] = {
        "case_name": "tc_57_large_dom_specific_element",
        "case_type": "structured",
        "description": "Access a specific deeply nested element in large DOM",
        "steps": [
            {"action": "goto", "selector": "", "value": f"{BASE}/large"},
        ],
        "assertion": {"type": "visible", "expected": "#sibling-50.50 element accessible"},
    }

    # ── tc_58: New window open ──
    plans["tc_58"] = {
        "case_name": "tc_58_new_window_open",
        "case_type": "structured",
        "description": "Click link to open a new window",
        "steps": [
            {"action": "goto", "selector": "", "value": f"{BASE}/windows"},
            {"action": "click", "selector": ".example a", "value": "new-window"},
        ],
        "assertion": {"type": "visible", "expected": "new window opened"},
    }

    # ── tc_59: New window text ──
    plans["tc_59"] = {
        "case_name": "tc_59_new_window_text",
        "case_type": "structured",
        "description": "Verify text in newly opened window",
        "steps": [
            {"action": "goto", "selector": "", "value": f"{BASE}/windows"},
            {"action": "click", "selector": ".example a", "value": "new-window"},
        ],
        "assertion": {"type": "text", "expected": "New Window"},
    }

    # ── tc_60: New window return to original ──
    plans["tc_60"] = {
        "case_name": "tc_60_new_window_return",
        "case_type": "structured",
        "description": "Open new window then switch back to original",
        "steps": [
            {"action": "goto", "selector": "", "value": f"{BASE}/windows"},
            {"action": "click", "selector": ".example a", "value": "new-window"},
            {"action": "evaluate", "selector": "", "value": "switch back to original window"},
        ],
        "assertion": {"type": "url", "expected": "/windows"},
    }

    # ── tc_61: Notification message display ──
    plans["tc_61"] = {
        "case_name": "tc_61_notification_message_display",
        "case_type": "structured",
        "description": "Click link and verify notification message appears",
        "steps": [
            {"action": "goto", "selector": "", "value": f"{BASE}/notification_message"},
            {"action": "click", "selector": "a[href='/notification_message']", "value": ""},
        ],
        "assertion": {"type": "visible", "expected": "#flash notification visible"},
    }

    # ── tc_62: Notification message change on repeat ──
    plans["tc_62"] = {
        "case_name": "tc_62_notification_message_repeat",
        "case_type": "structured",
        "description": "Click multiple times and check notification messages",
        "steps": [
            {"action": "goto", "selector": "", "value": f"{BASE}/notification_message"},
            {"action": "click", "selector": "a[href='/notification_message']", "value": ""},
            {"action": "click", "selector": "a[href='/notification_message']", "value": ""},
        ],
        "assertion": {"type": "visible", "expected": "notification message displayed"},
    }

    # ── tc_63: Notification close button ──
    plans["tc_63"] = {
        "case_name": "tc_63_notification_close",
        "case_type": "structured",
        "description": "Close notification message via close link",
        "steps": [
            {"action": "goto", "selector": "", "value": f"{BASE}/notification_message"},
            {"action": "click", "selector": "a[href='/notification_message']", "value": ""},
            {"action": "click", "selector": "#flash .close", "value": ""},
        ],
        "assertion": {"type": "hidden", "expected": "notification message hidden"},
    }

    # ── tc_64: Redirect link click ──
    plans["tc_64"] = {
        "case_name": "tc_64_redirect_link_click",
        "case_type": "structured",
        "description": "Click redirect link and verify redirection",
        "steps": [
            {"action": "goto", "selector": "", "value": f"{BASE}/redirector"},
            {"action": "click", "selector": "#redirect", "value": ""},
        ],
        "assertion": {"type": "url", "expected": "/status_codes"},
    }

    # ── tc_65: Redirect final URL ──
    plans["tc_65"] = {
        "case_name": "tc_65_redirect_final_url",
        "case_type": "structured",
        "description": "Verify final URL after redirect chain",
        "steps": [
            {"action": "goto", "selector": "", "value": f"{BASE}/redirector"},
            {"action": "click", "selector": "#redirect", "value": ""},
        ],
        "assertion": {"type": "url", "expected": "/status_codes"},
    }

    # ── tc_66: Shadow DOM text access ──
    plans["tc_66"] = {
        "case_name": "tc_66_shadow_dom_text",
        "case_type": "structured",
        "description": "Access text inside shadow DOM",
        "steps": [
            {"action": "goto", "selector": "", "value": f"{BASE}/shadowdom"},
        ],
        "assertion": {"type": "text", "expected": "Let's have some different text!"},
    }

    # ── tc_67: Shadow DOM second element ──
    plans["tc_67"] = {
        "case_name": "tc_67_shadow_dom_second_element",
        "case_type": "structured",
        "description": "Access second shadow DOM element text",
        "steps": [
            {"action": "goto", "selector": "", "value": f"{BASE}/shadowdom"},
        ],
        "assertion": {"type": "text", "expected": "In a list!"},
    }

    # ── tc_68: Shifting content image list ──
    plans["tc_68"] = {
        "case_name": "tc_68_shifting_content_image_list",
        "case_type": "structured",
        "description": "Verify shifting content page shows links",
        "steps": [
            {"action": "goto", "selector": "", "value": f"{BASE}/shifting_content"},
        ],
        "assertion": {"type": "visible", "expected": "shifting content links present"},
    }

    # ── tc_69: Shifting content image position ──
    plans["tc_69"] = {
        "case_name": "tc_69_shifting_content_image_position",
        "case_type": "structured",
        "description": "Verify images shift position on reload",
        "steps": [
            {"action": "goto", "selector": "", "value": f"{BASE}/shifting_content/image"},
            {"action": "evaluate", "selector": "", "value": "capture image positions"},
            {"action": "goto", "selector": "", "value": f"{BASE}/shifting_content/image?mode=random"},
        ],
        "assertion": {"type": "visible", "expected": "images present on page"},
    }

    # ── tc_70: Shifting content list elements ──
    plans["tc_70"] = {
        "case_name": "tc_70_shifting_content_list",
        "case_type": "structured",
        "description": "Verify list elements exist on shifting content list page",
        "steps": [
            {"action": "goto", "selector": "", "value": f"{BASE}/shifting_content/list"},
        ],
        "assertion": {"type": "visible", "expected": "list items present"},
    }

    # ── tc_71: Slow resources load wait ──
    plans["tc_71"] = {
        "case_name": "tc_71_slow_resources_load",
        "case_type": "structured",
        "description": "Wait for slow resources page to fully load",
        "steps": [
            {"action": "goto", "selector": "", "value": f"{BASE}/slow"},
            {"action": "wait", "selector": "", "value": "networkidle"},
        ],
        "assertion": {"type": "visible", "expected": "page content loaded after delay"},
    }

    # ── tc_72: Status code 200 ──
    plans["tc_72"] = {
        "case_name": "tc_72_status_code_200",
        "case_type": "structured",
        "description": "Navigate to status code 200 page and verify",
        "steps": [
            {"action": "goto", "selector": "", "value": f"{BASE}/status_codes"},
            {"action": "click", "selector": "a[href='status_codes/200']", "value": ""},
        ],
        "assertion": {"type": "text", "expected": "200"},
    }

    # ── tc_73: Status code 301 ──
    plans["tc_73"] = {
        "case_name": "tc_73_status_code_301",
        "case_type": "structured",
        "description": "Navigate to status code 301 page and verify",
        "steps": [
            {"action": "goto", "selector": "", "value": f"{BASE}/status_codes"},
            {"action": "click", "selector": "a[href='status_codes/301']", "value": ""},
        ],
        "assertion": {"type": "text", "expected": "301"},
    }

    # ── tc_74: Status code 404 ──
    plans["tc_74"] = {
        "case_name": "tc_74_status_code_404",
        "case_type": "structured",
        "description": "Navigate to status code 404 page and verify",
        "steps": [
            {"action": "goto", "selector": "", "value": f"{BASE}/status_codes"},
            {"action": "click", "selector": "a[href='status_codes/404']", "value": ""},
        ],
        "assertion": {"type": "text", "expected": "404"},
    }

    # ── tc_75: Status code 500 ──
    plans["tc_75"] = {
        "case_name": "tc_75_status_code_500",
        "case_type": "structured",
        "description": "Navigate to status code 500 page and verify",
        "steps": [
            {"action": "goto", "selector": "", "value": f"{BASE}/status_codes"},
            {"action": "click", "selector": "a[href='status_codes/500']", "value": ""},
        ],
        "assertion": {"type": "text", "expected": "500"},
    }

    # ── tc_76: Typos page text exists ──
    plans["tc_76"] = {
        "case_name": "tc_76_typos_text_exists",
        "case_type": "structured",
        "description": "Verify text content exists on typos page",
        "steps": [
            {"action": "goto", "selector": "", "value": f"{BASE}/typos"},
        ],
        "assertion": {"type": "visible", "expected": "paragraph text visible"},
    }

    # ── tc_77: Typos page detect typo ──
    plans["tc_77"] = {
        "case_name": "tc_77_typos_detect",
        "case_type": "structured",
        "description": "Detect typos in the page text content",
        "steps": [
            {"action": "goto", "selector": "", "value": f"{BASE}/typos"},
        ],
        "assertion": {"type": "text", "expected": "Sometimes you'll see a typo"},
    }

    # ── tc_78: TinyMCE editor load ──
    plans["tc_78"] = {
        "case_name": "tc_78_tinymce_editor_load",
        "case_type": "structured",
        "description": "Verify TinyMCE editor loads on page",
        "steps": [
            {"action": "goto", "selector": "", "value": f"{BASE}/tinymce"},
            {"action": "wait", "selector": "iframe#mce_0_ifr", "value": ""},
        ],
        "assertion": {"type": "visible", "expected": "TinyMCE editor iframe visible"},
    }

    # ── tc_79: TinyMCE editor text input ──
    plans["tc_79"] = {
        "case_name": "tc_79_tinymce_editor_input",
        "case_type": "structured",
        "description": "Type text into TinyMCE editor",
        "steps": [
            {"action": "goto", "selector": "", "value": f"{BASE}/tinymce"},
            {"action": "wait", "selector": "iframe#mce_0_ifr", "value": ""},
            {"action": "fill", "selector": "iframe#mce_0_ifr >> #tinymce", "value": "Hello TinyMCE"},
        ],
        "assertion": {"type": "text", "expected": "Hello TinyMCE"},
    }

    # ── tc_80: TinyMCE editor default text ──
    plans["tc_80"] = {
        "case_name": "tc_80_tinymce_default_text",
        "case_type": "structured",
        "description": "Read default text from TinyMCE editor",
        "steps": [
            {"action": "goto", "selector": "", "value": f"{BASE}/tinymce"},
            {"action": "wait", "selector": "iframe#mce_0_ifr", "value": ""},
        ],
        "assertion": {"type": "text", "expected": "Your content goes here."},
    }

    # ── tc_81: Login empty fields submit ──
    plans["tc_81"] = {
        "case_name": "tc_81_login_empty_fields",
        "case_type": "structured",
        "description": "Submit login form with empty fields",
        "steps": [
            {"action": "goto", "selector": "", "value": f"{BASE}/login"},
            {"action": "click", "selector": "button.radius", "value": ""},
        ],
        "assertion": {"type": "text", "expected": "Your username is invalid!"},
    }

    # ── tc_82: Login username only ──
    plans["tc_82"] = {
        "case_name": "tc_82_login_username_only",
        "case_type": "structured",
        "description": "Submit login with only username filled",
        "steps": [
            {"action": "goto", "selector": "", "value": f"{BASE}/login"},
            {"action": "fill", "selector": "#username", "value": "tomsmith"},
            {"action": "click", "selector": "button.radius", "value": ""},
        ],
        "assertion": {"type": "text", "expected": "Your password is invalid!"},
    }

    # ── tc_83: Login password only ──
    plans["tc_83"] = {
        "case_name": "tc_83_login_password_only",
        "case_type": "structured",
        "description": "Submit login with only password filled",
        "steps": [
            {"action": "goto", "selector": "", "value": f"{BASE}/login"},
            {"action": "fill", "selector": "#password", "value": "SuperSecretPassword!"},
            {"action": "click", "selector": "button.radius", "value": ""},
        ],
        "assertion": {"type": "text", "expected": "Your username is invalid!"},
    }

    # ── tc_84: SQL Injection login ──
    plans["tc_84"] = {
        "case_name": "tc_84_sql_injection_login",
        "case_type": "structured",
        "description": "Attempt SQL injection in login fields",
        "steps": [
            {"action": "goto", "selector": "", "value": f"{BASE}/login"},
            {"action": "fill", "selector": "#username", "value": "' OR '1'='1"},
            {"action": "fill", "selector": "#password", "value": "' OR '1'='1"},
            {"action": "click", "selector": "button.radius", "value": ""},
        ],
        "assertion": {"type": "text", "expected": "Your username is invalid!"},
    }

    # ── tc_85: XSS login attempt ──
    plans["tc_85"] = {
        "case_name": "tc_85_xss_login_attempt",
        "case_type": "structured",
        "description": "Attempt XSS script injection in login fields",
        "steps": [
            {"action": "goto", "selector": "", "value": f"{BASE}/login"},
            {"action": "fill", "selector": "#username", "value": "<script>alert('xss')</script>"},
            {"action": "fill", "selector": "#password", "value": "test"},
            {"action": "click", "selector": "button.radius", "value": ""},
        ],
        "assertion": {"type": "text", "expected": "Your username is invalid!"},
    }

    # ── tc_86: Checkbox 1 toggle ──
    plans["tc_86"] = {
        "case_name": "tc_86_checkbox_1_toggle",
        "case_type": "structured",
        "description": "Toggle first checkbox and verify state",
        "steps": [
            {"action": "goto", "selector": "", "value": f"{BASE}/checkboxes"},
            {"action": "click", "selector": "#checkboxes input:nth-of-type(1)", "value": ""},
        ],
        "assertion": {"type": "attribute", "expected": "checkbox1=checked"},
    }

    # ── tc_87: Checkbox 2 toggle ──
    plans["tc_87"] = {
        "case_name": "tc_87_checkbox_2_toggle",
        "case_type": "structured",
        "description": "Toggle second checkbox and verify state",
        "steps": [
            {"action": "goto", "selector": "", "value": f"{BASE}/checkboxes"},
            {"action": "click", "selector": "#checkboxes input:nth-of-type(2)", "value": ""},
        ],
        "assertion": {"type": "attribute", "expected": "checkbox2=unchecked"},
    }

    # ── tc_88: Checkbox initial state ──
    plans["tc_88"] = {
        "case_name": "tc_88_checkbox_initial_state",
        "case_type": "structured",
        "description": "Verify initial checkbox states without interaction",
        "steps": [
            {"action": "goto", "selector": "", "value": f"{BASE}/checkboxes"},
        ],
        "assertion": {"type": "attribute", "expected": "checkbox1=unchecked,checkbox2=checked"},
    }

    # ── tc_89: Dropdown Option 1 ──
    plans["tc_89"] = {
        "case_name": "tc_89_dropdown_option_1",
        "case_type": "structured",
        "description": "Select Option 1 from dropdown",
        "steps": [
            {"action": "goto", "selector": "", "value": f"{BASE}/dropdown"},
            {"action": "select", "selector": "#dropdown", "value": "1"},
        ],
        "assertion": {"type": "attribute", "expected": "value=1"},
    }

    # ── tc_90: Dropdown Option 2 ──
    plans["tc_90"] = {
        "case_name": "tc_90_dropdown_option_2",
        "case_type": "structured",
        "description": "Select Option 2 from dropdown",
        "steps": [
            {"action": "goto", "selector": "", "value": f"{BASE}/dropdown"},
            {"action": "select", "selector": "#dropdown", "value": "2"},
        ],
        "assertion": {"type": "attribute", "expected": "value=2"},
    }

    # ── tc_91: Dropdown default value ──
    plans["tc_91"] = {
        "case_name": "tc_91_dropdown_default_value",
        "case_type": "structured",
        "description": "Verify dropdown default selected value",
        "steps": [
            {"action": "goto", "selector": "", "value": f"{BASE}/dropdown"},
        ],
        "assertion": {"type": "attribute", "expected": "selectedIndex=0 (Please select an option)"},
    }

    # ── tc_92: Multiple element add ──
    plans["tc_92"] = {
        "case_name": "tc_92_multiple_element_add",
        "case_type": "structured",
        "description": "Add multiple elements and verify count",
        "steps": [
            {"action": "goto", "selector": "", "value": f"{BASE}/add_remove_elements/"},
            {"action": "click", "selector": "button[onclick='addElement()']", "value": ""},
            {"action": "click", "selector": "button[onclick='addElement()']", "value": ""},
            {"action": "click", "selector": "button[onclick='addElement()']", "value": ""},
            {"action": "click", "selector": "button[onclick='addElement()']", "value": ""},
            {"action": "click", "selector": "button[onclick='addElement()']", "value": ""},
        ],
        "assertion": {"type": "visible", "expected": "5 Delete buttons present"},
    }

    # ── tc_93: Delete all added elements ──
    plans["tc_93"] = {
        "case_name": "tc_93_delete_all_elements",
        "case_type": "structured",
        "description": "Add elements then delete all of them",
        "steps": [
            {"action": "goto", "selector": "", "value": f"{BASE}/add_remove_elements/"},
            {"action": "click", "selector": "button[onclick='addElement()']", "value": ""},
            {"action": "click", "selector": "button[onclick='addElement()']", "value": ""},
            {"action": "click", "selector": "button[onclick='addElement()']", "value": ""},
            {"action": "click", "selector": "#elements .added-manually:first-child", "value": ""},
            {"action": "click", "selector": "#elements .added-manually:first-child", "value": ""},
            {"action": "click", "selector": "#elements .added-manually:first-child", "value": ""},
        ],
        "assertion": {"type": "hidden", "expected": "no Delete buttons remaining"},
    }

    # ── tc_94: Add delete repeat ──
    plans["tc_94"] = {
        "case_name": "tc_94_add_delete_repeat",
        "case_type": "structured",
        "description": "Repeatedly add and delete elements",
        "steps": [
            {"action": "goto", "selector": "", "value": f"{BASE}/add_remove_elements/"},
            {"action": "click", "selector": "button[onclick='addElement()']", "value": ""},
            {"action": "click", "selector": "#elements .added-manually:first-child", "value": ""},
            {"action": "click", "selector": "button[onclick='addElement()']", "value": ""},
            {"action": "click", "selector": "#elements .added-manually:first-child", "value": ""},
        ],
        "assertion": {"type": "hidden", "expected": "no Delete buttons remaining after repeat"},
    }

    # ── tc_95: User 1 profile hover ──
    plans["tc_95"] = {
        "case_name": "tc_95_user_1_profile_hover",
        "case_type": "structured",
        "description": "Hover over first user avatar to show profile info",
        "steps": [
            {"action": "goto", "selector": "", "value": f"{BASE}/hovers"},
            {"action": "hover", "selector": ".figure:nth-child(3)", "value": ""},
        ],
        "assertion": {"type": "visible", "expected": "name: user1 displayed"},
    }

    # ── tc_96: User 2 profile hover ──
    plans["tc_96"] = {
        "case_name": "tc_96_user_2_profile_hover",
        "case_type": "structured",
        "description": "Hover over second user avatar to show profile info",
        "steps": [
            {"action": "goto", "selector": "", "value": f"{BASE}/hovers"},
            {"action": "hover", "selector": ".figure:nth-child(4)", "value": ""},
        ],
        "assertion": {"type": "visible", "expected": "name: user2 displayed"},
    }

    # ── tc_97: User 3 hover profile link ──
    plans["tc_97"] = {
        "case_name": "tc_97_user_3_hover_profile_link",
        "case_type": "structured",
        "description": "Hover over third user and verify profile link",
        "steps": [
            {"action": "goto", "selector": "", "value": f"{BASE}/hovers"},
            {"action": "hover", "selector": ".figure:nth-child(5)", "value": ""},
        ],
        "assertion": {"type": "visible", "expected": "View profile link for user3"},
    }

    # ── tc_98: Dynamic Loading Example 1 ──
    plans["tc_98"] = {
        "case_name": "tc_98_dynamic_loading_hidden_to_visible",
        "case_type": "structured",
        "description": "Click Start on Example 1 to reveal hidden element",
        "steps": [
            {"action": "goto", "selector": "", "value": f"{BASE}/dynamic_loading/1"},
            {"action": "click", "selector": "#start button", "value": ""},
            {"action": "wait", "selector": "#finish", "value": ""},
        ],
        "assertion": {"type": "text", "expected": "Hello World!"},
    }

    # ── tc_99: Dynamic Loading Example 2 ──
    plans["tc_99"] = {
        "case_name": "tc_99_dynamic_loading_rendered",
        "case_type": "structured",
        "description": "Click Start on Example 2 to render element",
        "steps": [
            {"action": "goto", "selector": "", "value": f"{BASE}/dynamic_loading/2"},
            {"action": "click", "selector": "#start button", "value": ""},
            {"action": "wait", "selector": "#finish", "value": ""},
        ],
        "assertion": {"type": "text", "expected": "Hello World!"},
    }

    # ── tc_100: Dynamic Loading loading indicator ──
    plans["tc_100"] = {
        "case_name": "tc_100_dynamic_loading_indicator",
        "case_type": "structured",
        "description": "Verify loading indicator appears and disappears",
        "steps": [
            {"action": "goto", "selector": "", "value": f"{BASE}/dynamic_loading/1"},
            {"action": "click", "selector": "#start button", "value": ""},
            {"action": "wait", "selector": "#loading", "value": "visible"},
            {"action": "wait", "selector": "#loading", "value": "hidden"},
            {"action": "wait", "selector": "#finish", "value": ""},
        ],
        "assertion": {"type": "text", "expected": "Hello World!"},
    }

    # ── tc_101: Table Last Name sort ──
    plans["tc_101"] = {
        "case_name": "tc_101_table_last_name_sort",
        "case_type": "structured",
        "description": "Sort table by Last Name column ascending",
        "steps": [
            {"action": "goto", "selector": "", "value": f"{BASE}/tables"},
            {"action": "click", "selector": "#table1 thead tr th:nth-child(1)", "value": ""},
        ],
        "assertion": {"type": "text", "expected": "Last Name sorted ascending"},
    }

    # ── tc_102: Table First Name sort ──
    plans["tc_102"] = {
        "case_name": "tc_102_table_first_name_sort",
        "case_type": "structured",
        "description": "Sort table by First Name column ascending",
        "steps": [
            {"action": "goto", "selector": "", "value": f"{BASE}/tables"},
            {"action": "click", "selector": "#table1 thead tr th:nth-child(2)", "value": ""},
        ],
        "assertion": {"type": "text", "expected": "First Name sorted ascending"},
    }

    # ── tc_103: Table Email sort ──
    plans["tc_103"] = {
        "case_name": "tc_103_table_email_sort",
        "case_type": "structured",
        "description": "Sort table by Email column ascending",
        "steps": [
            {"action": "goto", "selector": "", "value": f"{BASE}/tables"},
            {"action": "click", "selector": "#table1 thead tr th:nth-child(3)", "value": ""},
        ],
        "assertion": {"type": "text", "expected": "Email sorted ascending"},
    }

    # ── tc_104: Table Due sort ──
    plans["tc_104"] = {
        "case_name": "tc_104_table_due_sort",
        "case_type": "structured",
        "description": "Sort table by Due column ascending",
        "steps": [
            {"action": "goto", "selector": "", "value": f"{BASE}/tables"},
            {"action": "click", "selector": "#table1 thead tr th:nth-child(4)", "value": ""},
        ],
        "assertion": {"type": "text", "expected": "Due sorted ascending"},
    }

    # ── tc_105: Table Web Site sort ──
    plans["tc_105"] = {
        "case_name": "tc_105_table_web_site_sort",
        "case_type": "structured",
        "description": "Sort table by Web Site column ascending",
        "steps": [
            {"action": "goto", "selector": "", "value": f"{BASE}/tables"},
            {"action": "click", "selector": "#table1 thead tr th:nth-child(5)", "value": ""},
        ],
        "assertion": {"type": "text", "expected": "Web Site sorted ascending"},
    }

    # ── tc_106: Enter key detection ──
    plans["tc_106"] = {
        "case_name": "tc_106_enter_key_detection",
        "case_type": "structured",
        "description": "Press Enter key and verify detection",
        "steps": [
            {"action": "goto", "selector": "", "value": f"{BASE}/key_presses"},
            {"action": "click", "selector": "#target", "value": ""},
            {"action": "press", "selector": "#target", "value": "Enter"},
        ],
        "assertion": {"type": "text", "expected": "You entered: ENTER"},
    }

    # ── tc_107: Escape key detection ──
    plans["tc_107"] = {
        "case_name": "tc_107_escape_key_detection",
        "case_type": "structured",
        "description": "Press Escape key and verify detection",
        "steps": [
            {"action": "goto", "selector": "", "value": f"{BASE}/key_presses"},
            {"action": "click", "selector": "#target", "value": ""},
            {"action": "press", "selector": "#target", "value": "Escape"},
        ],
        "assertion": {"type": "text", "expected": "You entered: ESCAPE"},
    }

    # ── tc_108: Tab key detection ──
    plans["tc_108"] = {
        "case_name": "tc_108_tab_key_detection",
        "case_type": "structured",
        "description": "Press Tab key and verify detection",
        "steps": [
            {"action": "goto", "selector": "", "value": f"{BASE}/key_presses"},
            {"action": "click", "selector": "#target", "value": ""},
            {"action": "press", "selector": "#target", "value": "Tab"},
        ],
        "assertion": {"type": "text", "expected": "You entered: TAB"},
    }

    # ── tc_109: Dynamic Controls checkbox remove then re-add ──
    plans["tc_109"] = {
        "case_name": "tc_109_dynamic_controls_checkbox_remove_readd",
        "case_type": "structured",
        "description": "Remove checkbox then add it back",
        "steps": [
            {"action": "goto", "selector": "", "value": f"{BASE}/dynamic_controls"},
            {"action": "click", "selector": "#checkbox-example button", "value": ""},
            {"action": "wait", "selector": "#message", "value": ""},
            {"action": "click", "selector": "#checkbox-example button", "value": ""},
            {"action": "wait", "selector": "#checkbox", "value": ""},
        ],
        "assertion": {"type": "visible", "expected": "checkbox re-added"},
    }

    # ── tc_110: Dynamic Controls enable then disable ──
    plans["tc_110"] = {
        "case_name": "tc_110_dynamic_controls_enable_disable",
        "case_type": "structured",
        "description": "Enable input then disable it again",
        "steps": [
            {"action": "goto", "selector": "", "value": f"{BASE}/dynamic_controls"},
            {"action": "click", "selector": "#input-example button", "value": ""},
            {"action": "wait", "selector": "#message", "value": ""},
            {"action": "click", "selector": "#input-example button", "value": ""},
            {"action": "wait", "selector": "#message", "value": ""},
        ],
        "assertion": {"type": "attribute", "expected": "input disabled again"},
    }

    # ── tc_111: Dynamic Controls disabled input attempt ──
    plans["tc_111"] = {
        "case_name": "tc_111_dynamic_controls_disabled_input",
        "case_type": "structured",
        "description": "Verify input field is disabled initially",
        "steps": [
            {"action": "goto", "selector": "", "value": f"{BASE}/dynamic_controls"},
        ],
        "assertion": {"type": "attribute", "expected": "input[type=text] is disabled"},
    }

    # ── tc_112: Dynamic Controls message verify ──
    plans["tc_112"] = {
        "case_name": "tc_112_dynamic_controls_message",
        "case_type": "structured",
        "description": "Verify message appears after dynamic control action",
        "steps": [
            {"action": "goto", "selector": "", "value": f"{BASE}/dynamic_controls"},
            {"action": "click", "selector": "#checkbox-example button", "value": ""},
            {"action": "wait", "selector": "#message", "value": ""},
        ],
        "assertion": {"type": "text", "expected": "It's gone!"},
    }

    # ── tc_113: JS Prompt cancel ──
    plans["tc_113"] = {
        "case_name": "tc_113_js_prompt_cancel",
        "case_type": "structured",
        "description": "Click JS Prompt and cancel the dialog",
        "steps": [
            {"action": "goto", "selector": "", "value": f"{BASE}/javascript_alerts"},
            {"action": "click", "selector": "button[onclick='jsPrompt()']", "value": "dialog:dismiss"},
        ],
        "assertion": {"type": "text", "expected": "You entered: null"},
    }

    # ── tc_114: JS Prompt empty value ──
    plans["tc_114"] = {
        "case_name": "tc_114_js_prompt_empty",
        "case_type": "structured",
        "description": "Click JS Prompt and confirm with empty input",
        "steps": [
            {"action": "goto", "selector": "", "value": f"{BASE}/javascript_alerts"},
            {"action": "click", "selector": "button[onclick='jsPrompt()']", "value": "dialog:accept:"},
        ],
        "assertion": {"type": "text", "expected": "You entered:"},
    }

    # ── tc_115: JS Alert text verify ──
    plans["tc_115"] = {
        "case_name": "tc_115_js_alert_text",
        "case_type": "structured",
        "description": "Verify JS Alert dialog text content",
        "steps": [
            {"action": "goto", "selector": "", "value": f"{BASE}/javascript_alerts"},
            {"action": "click", "selector": "button[onclick='jsAlert()']", "value": ""},
        ],
        "assertion": {"type": "text", "expected": "I am a JS Alert"},
    }

    # ── tc_116: Upload without file selection ──
    plans["tc_116"] = {
        "case_name": "tc_116_upload_no_file",
        "case_type": "structured",
        "description": "Click upload button without selecting a file",
        "steps": [
            {"action": "goto", "selector": "", "value": f"{BASE}/upload"},
            {"action": "click", "selector": "#file-submit", "value": ""},
        ],
        "assertion": {"type": "text", "expected": "Internal Server Error or no file uploaded"},
    }

    # ── tc_117: Upload page elements verify ──
    plans["tc_117"] = {
        "case_name": "tc_117_upload_page_elements",
        "case_type": "structured",
        "description": "Verify upload page has file input and submit button",
        "steps": [
            {"action": "goto", "selector": "", "value": f"{BASE}/upload"},
        ],
        "assertion": {"type": "visible", "expected": "#file-upload and #file-submit visible"},
    }

    # ── tc_118: Slider minimum value ──
    plans["tc_118"] = {
        "case_name": "tc_118_slider_min_value",
        "case_type": "structured",
        "description": "Set horizontal slider to minimum value",
        "steps": [
            {"action": "goto", "selector": "", "value": f"{BASE}/horizontal_slider"},
            {"action": "fill", "selector": "input[type='range']", "value": "0"},
        ],
        "assertion": {"type": "text", "expected": "0"},
    }

    # ── tc_119: Slider maximum value ──
    plans["tc_119"] = {
        "case_name": "tc_119_slider_max_value",
        "case_type": "structured",
        "description": "Set horizontal slider to maximum value",
        "steps": [
            {"action": "goto", "selector": "", "value": f"{BASE}/horizontal_slider"},
            {"action": "fill", "selector": "input[type='range']", "value": "5"},
        ],
        "assertion": {"type": "text", "expected": "5"},
    }

    # ── tc_120: Number input negative ──
    plans["tc_120"] = {
        "case_name": "tc_120_number_input_negative",
        "case_type": "structured",
        "description": "Enter a negative number in the input field",
        "steps": [
            {"action": "goto", "selector": "", "value": f"{BASE}/inputs"},
            {"action": "fill", "selector": "input[type='number']", "value": "-5"},
        ],
        "assertion": {"type": "attribute", "expected": "value=-5"},
    }

    return plans


def main():
    with open(PIPELINE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    plans_by_id = make_plan()

    # Build plan array in test_cases order
    plan_list = []
    tc_ids = [tc['id'] for tc in data['test_cases']]
    missing = []
    for tc_id in tc_ids:
        if tc_id in plans_by_id:
            plan_list.append(plans_by_id[tc_id])
        else:
            missing.append(tc_id)

    if missing:
        print(f"ERROR: Missing plans for {len(missing)} cases: {missing}")
        return

    # Update pipeline.json -- only modify "plan" and "step"
    data['plan'] = plan_list
    data['step'] = 'planned'

    with open(PIPELINE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"SUCCESS: Generated {len(plan_list)} plan entries.")
    print(f"Step updated to: 'planned'")

    # Verify case_name prefixes match tc_ids
    for i, p in enumerate(plan_list):
        tc_id = tc_ids[i]
        num = int(tc_id.split('_')[1])
        expected_prefix = f"tc_{num:02d}_" if num < 100 else f"tc_{num}_"
        assert p['case_name'].startswith(expected_prefix) or \
               p['case_name'].startswith(f"tc_{num}_"), \
               f"Mismatch: {tc_id} -> {p['case_name']}"
    print("All case_name prefixes verified.")


if __name__ == '__main__':
    main()
