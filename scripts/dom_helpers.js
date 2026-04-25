// DOM 공통 유틸 — isVisible, esc, getSelectorsSimple
// 01_analyze.py의 _js()가 각 JS 스크립트 앞에 자동 주입한다.

function isVisible(el) {
    const s = window.getComputedStyle(el);
    if (s.display === 'none' || s.visibility === 'hidden' || s.opacity === '0') return false;
    if (el.offsetWidth <= 0 || el.offsetHeight <= 0) return false;
    if (s.clipPath === 'inset(100%)') return false;
    if (s.clip === 'rect(0px, 0px, 0px, 0px)') return false;
    const rect = el.getBoundingClientRect();
    if (rect.right < 0 || rect.bottom < 0) return false;
    return true;
}

function esc(v) { return (v || '').replace(/\\/g, '\\\\').replace(/"/g, '\\"'); }

function getSelectorsSimple(el) {
    const s = {};
    const tag = el.tagName.toLowerCase();
    const text = (el.innerText || el.textContent || '').trim().slice(0, 60);
    if (el.id) s.id = '#' + el.id;
    for (const attr of ['data-testid', 'data-test', 'data-cy', 'data-qa']) {
        const v = el.getAttribute(attr);
        if (v) { s.testid = `[${attr}="${esc(v)}"]`; break; }
    }
    const aria = el.getAttribute('aria-label');
    if (aria) s.aria_label = `[aria-label="${esc(aria)}"]`;
    const role = el.getAttribute('role');
    if (role) s.role = aria ? `[role="${role}"][aria-label="${esc(aria)}"]` : `[role="${role}"]`;
    if (text && ['button', 'a', 'li', 'span', 'div'].includes(tag)) s.text = text;
    if (el.name) s.name = `[name="${esc(el.name)}"]`;
    return s;
}
