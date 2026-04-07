"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_34_drag_and_drop_b_to_a (tc_34)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
BASE_URL = "https://the-internet.herokuapp.com/"


def test_tc_34_drag_and_drop_b_to_a(page):
    """컬럼 B를 A로 드래그 앤 드롭 (JS 시뮬레이션) 후 위치 교환 확인"""
    page.goto("https://the-internet.herokuapp.com/drag_and_drop")
    page.wait_for_selector("#column-b", state="visible")

    page.evaluate("""() => {
        function simulateDragDrop(src, dst) {
            var dt = {
                data: {},
                setData: function(k, v) { this.data[k] = v; },
                getData: function(k) { return this.data[k]; }
            };
            function fireEvent(el, type) {
                var e = document.createEvent('DragEvent');
                e.initEvent(type, true, true);
                Object.defineProperty(e, 'dataTransfer', { value: dt });
                el.dispatchEvent(e);
            }
            fireEvent(src, 'dragstart');
            fireEvent(dst, 'dragenter');
            fireEvent(dst, 'dragover');
            fireEvent(dst, 'drop');
            fireEvent(src, 'dragend');
        }
        var src = document.querySelector('#column-b');
        var dst = document.querySelector('#column-a');
        simulateDragDrop(src, dst);
    }""")

    page.wait_for_timeout(500)
    col_a_text = page.locator("#column-a header").inner_text()
    col_b_text = page.locator("#column-b header").inner_text()
    assert col_a_text.strip() == "B", f"Expected column-a to show B, got: {col_a_text}"
    assert col_b_text.strip() == "A", f"Expected column-b to show A, got: {col_b_text}"
