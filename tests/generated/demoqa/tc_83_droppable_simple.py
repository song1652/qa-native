from playwright.sync_api import Page, expect

BASE_URL = "https://demoqa.com"


def test_droppable_simple(page: Page):
    page.goto(f"{BASE_URL}/droppable", wait_until="domcontentloaded")
    page.wait_for_timeout(2000)

    # Remove ads/footer
    page.evaluate("""
        document.querySelectorAll(
            'ins.adsbygoogle, iframe[src*=google], iframe[src*=doubleclick], footer, #fixedban'
        ).forEach(e => e.remove())
    """)

    # Click Simple tab (it may already be active)
    simple_tab = page.locator("#droppableExample-tab-simple")
    expect(simple_tab).to_be_visible(timeout=10000)
    simple_tab.click()
    page.wait_for_timeout(500)

    # Scope to the active Simple pane to avoid duplicate ID issues
    simple_pane = page.locator("#droppableExample-tabpane-simple")
    expect(simple_pane).to_be_visible(timeout=10000)

    drag_me = simple_pane.locator("#draggable")
    drop_here = simple_pane.locator("#droppable")

    expect(drag_me).to_be_visible(timeout=10000)
    expect(drop_here).to_be_visible(timeout=10000)

    # Verify initial state - text is "Drop Here" (capital H)
    expect(drop_here).to_contain_text("Drop Here", timeout=5000)

    # Perform drag-and-drop using JS MouseEvent simulation
    page.evaluate("""
        () => {
            const pane = document.querySelector('#droppableExample-tabpane-simple');
            const dragEl = pane.querySelector('#draggable');
            const dropEl = pane.querySelector('#droppable');

            const dragRect = dragEl.getBoundingClientRect();
            const dropRect = dropEl.getBoundingClientRect();

            const startX = dragRect.left + dragRect.width / 2;
            const startY = dragRect.top + dragRect.height / 2;
            const endX = dropRect.left + dropRect.width / 2;
            const endY = dropRect.top + dropRect.height / 2;

            const steps = 20;
            const dx = (endX - startX) / steps;
            const dy = (endY - startY) / steps;

            dragEl.dispatchEvent(new MouseEvent('mousedown', {bubbles: true, clientX: startX, clientY: startY}));
            for (let i = 0; i <= steps; i++) {
                document.dispatchEvent(new MouseEvent('mousemove', {bubbles: true,
                    clientX: startX + dx * i, clientY: startY + dy * i}));
            }
            dropEl.dispatchEvent(new MouseEvent('mouseup', {bubbles: true, clientX: endX, clientY: endY}));
        }
    """)

    page.wait_for_timeout(1000)

    # Verify drop area text changed to "Dropped!"
    expect(drop_here).to_contain_text("Dropped!", timeout=5000)
