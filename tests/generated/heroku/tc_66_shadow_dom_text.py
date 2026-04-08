"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_66_shadow_dom_text (tc_66)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from pathlib import Path

BASE_URL = "https://the-internet.herokuapp.com/"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_tc_66_shadow_dom_text(page):
    """Shadow DOM 첫 번째 호스트 요소의 내부 텍스트 확인 (실제: My default text)"""
    page.goto("https://the-internet.herokuapp.com/shadowdom")
    page.wait_for_load_state("domcontentloaded")

    # First my-paragraph element: actual text is "My default text"
    # shadowRoot.innerText is undefined — use textContent (includes CSS)
    text = page.evaluate(
        "() => { const el = document.querySelectorAll('my-paragraph')[0]; return el.shadowRoot.textContent; }"
    )
    assert text is not None
    assert "My default text" in text
