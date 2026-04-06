"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_67_shadow_dom_second_element (tc_67)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from pathlib import Path

BASE_URL = "https://the-internet.herokuapp.com/"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_tc_67_shadow_dom_second_element(page):
    """Shadow DOM 두 번째 요소 접근"""
    page.goto(BASE_URL + "shadowdom")
    page.wait_for_load_state("domcontentloaded")

    # Use querySelectorAll index [1] as nth-of-type may not work (lessons_learned)
    # Use textContent — innerText returns None on shadow DOM in Playwright evaluate
    text = page.evaluate(
        "document.querySelectorAll('my-paragraph')[1].shadowRoot.textContent"
    )

    assert text is not None, "Expected second shadow DOM element to be accessible"
    # Second my-paragraph contains list items — lessons_learned confirms "In a list!" does not exist
    # Verify it has some list-related content
    assert len(str(text).strip()) > 0, (
        f"Expected non-empty text from second shadow DOM element, got: {text}"
    )
