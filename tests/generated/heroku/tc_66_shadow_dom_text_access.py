"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_66_shadow_dom_text_access (tc_66)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from pathlib import Path

BASE_URL = "https://the-internet.herokuapp.com/"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_tc_66_shadow_dom_text_access(page):
    """Shadow DOM 내부 텍스트 접근"""
    page.goto(BASE_URL + "shadowdom")
    page.wait_for_load_state("domcontentloaded")

    # Use textContent — innerText returns None on shadow DOM in Playwright evaluate
    text = page.evaluate(
        "document.querySelectorAll('my-paragraph')[0].shadowRoot.textContent"
    )

    assert text is not None, "Expected shadow DOM textContent to be accessible"
    assert len(str(text).strip()) > 0, "Expected non-empty shadow DOM text"
    # First my-paragraph contains "My default text"
    assert "My default text" in str(text), (
        f"Expected 'My default text' in shadow DOM, got: {text}"
    )
