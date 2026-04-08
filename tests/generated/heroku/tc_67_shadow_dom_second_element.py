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
    """Shadow DOM 두 번째 호스트 요소의 리스트 항목 텍스트 확인"""
    page.goto("https://the-internet.herokuapp.com/shadowdom")
    page.wait_for_load_state("domcontentloaded")

    # Second my-paragraph element contains list items including "In a list!"
    # Use innerHTML of the host element (light DOM slot content)
    text = page.evaluate(
        "() => { const el = document.querySelectorAll('my-paragraph')[1]; return el.innerHTML; }"
    )
    assert text is not None
    assert "In a list!" in text
