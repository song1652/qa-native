"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_34_drag_and_drop_b_to_a (tc_34)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_tc_34_drag_and_drop_b_to_a(page):
    """드래그 앤 드롭 B에서 A로"""
    page.goto(BASE_URL + "drag_and_drop")
    expect(page.locator("#column-a")).to_be_visible()
    expect(page.locator("#column-b")).to_be_visible()

    # HTML5 drag and drop requires JS simulation with custom events
    page.evaluate("""
        () => {
            function simulateDragDrop(sourceNode, destinationNode) {
                var EVENT_TYPES = { DRAG_END: 'dragend', DRAG_START: 'dragstart', DROP: 'drop' };
                function createCustomEvent(type) {
                    var event = new CustomEvent("Event", { bubbles: true, cancelable: true });
                    event.initCustomEvent(type, true, true, null);
                    event.dataTransfer = {
                        data: {},
                        setData: function(type, val) { this.data[type] = val; },
                        getData: function(type) { return this.data[type]; }
                    };
                    return event;
                }
                var event = createCustomEvent(EVENT_TYPES.DRAG_START);
                sourceNode.dispatchEvent(event);
                var dropEvent = createCustomEvent(EVENT_TYPES.DROP);
                dropEvent.dataTransfer = event.dataTransfer;
                destinationNode.dispatchEvent(dropEvent);
                var dragEndEvent = createCustomEvent(EVENT_TYPES.DRAG_END);
                sourceNode.dispatchEvent(dragEndEvent);
            }
            simulateDragDrop(
                document.querySelector('#column-b'),
                document.querySelector('#column-a')
            );
        }
    """)
    page.wait_for_timeout(500)

    col_a_text = page.locator("#column-a header").inner_text()
    col_b_text = page.locator("#column-b header").inner_text()
    assert col_a_text == "B", f"Expected column-a to show 'B', got: '{col_a_text}'"
    assert col_b_text == "A", f"Expected column-b to show 'A', got: '{col_b_text}'"
