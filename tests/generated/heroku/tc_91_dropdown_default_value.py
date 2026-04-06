from playwright.sync_api import Page, expect

BASE_URL = "https://the-internet.herokuapp.com/"


def test_dropdown_default_value(page: Page):
    page.goto(BASE_URL + "dropdown")
    page.wait_for_load_state("domcontentloaded")

    # Verify the default selected option text via JS (option element may not be "visible" in Playwright)
    selected_text = page.evaluate(
        "() => { const sel = document.querySelector('#dropdown'); "
        "return sel ? sel.options[sel.selectedIndex].text : ''; }"
    )
    assert "Please select an option" in selected_text, (
        f"Expected default option to contain 'Please select an option', got: {selected_text!r}"
    )

    # Verify the disabled placeholder option exists in DOM
    disabled_option = page.locator("#dropdown option[disabled]")
    assert disabled_option.count() > 0, "Expected a disabled placeholder option to exist"
    expect(disabled_option).to_contain_text(
        "Please select an option", timeout=5000
    )
