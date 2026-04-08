"""
Step 1 — 페이지 DOM 분석
LLM 없음. Playwright로 직접 DOM 추출.
결과를 state.json의 dom_cache_key에 참조 저장.

Claude Code는 이 스크립트 실행 후
dom_info를 읽고 테스트 전략(plan)을 직접 수립해서 state.json에 저장한다.
"""
import asyncio
import hashlib
import re
import sys
from pathlib import Path
from playwright.async_api import async_playwright
from _paths import (
    PIPELINE_STATE, DOM_CACHE_DIR,
    read_state, write_state,
    get_cached_dom, save_dom_cache,
)


# ---------------------------------------------------------------------------
# DOM 추출 JS — analyze_all() 공유
# ---------------------------------------------------------------------------
DOM_EXTRACT_JS = """() => {
    function bestSelector(el) {
        if (el.id) return '#' + el.id;
        if (el.name) return `[name="${el.name}"]`;
        const cls = [...el.classList].filter(c => !c.match(/^(ng-|_|js-)/)).slice(0,2).join('.');
        return cls ? el.tagName.toLowerCase() + '.' + cls : el.tagName.toLowerCase();
    }

    const inputs = [...document.querySelectorAll('input:not([type=hidden]), textarea, select')]
        .map(el => ({
            selector:    bestSelector(el),
            type:        el.type || el.tagName.toLowerCase(),
            name:        el.name || el.id || '',
            placeholder: el.placeholder || '',
            required:    el.required,
            visible:     el.offsetParent !== null
        })).filter(e => e.visible);

    const buttons = [...document.querySelectorAll('button, input[type=submit], input[type=button], [role=button]')]
        .map(el => ({
            selector: bestSelector(el),
            text:     (el.innerText || el.value || '').trim().slice(0, 50),
            type:     el.type || 'button',
            visible:  el.offsetParent !== null
        })).filter(e => e.visible);

    const errors = [...document.querySelectorAll(
        '[role=alert], [role=status], .error, .alert, .message, .invalid-feedback, [class*=error], [class*=alert]'
    )].map(el => ({
        selector: bestSelector(el),
        role:     el.getAttribute('role') || 'unknown',
        text:     el.innerText?.trim().slice(0, 80) || ''
    }));

    const links = [...document.querySelectorAll('a[href]')]
        .map(a => ({ text: a.innerText.trim().slice(0,30), href: a.href }))
        .filter(a => a.text).slice(0, 10);

    // React/UI 컴포넌트 추출
    const components = [];

    // Tabs (role=tab or data-toggle=tab)
    document.querySelectorAll('[role="tab"], [data-toggle="tab"], .nav-link').forEach(el => {
        components.push({
            type: 'tab',
            selector: bestSelector(el),
            text: (el.innerText || '').trim().slice(0, 50),
            active: el.classList.contains('active') || el.getAttribute('aria-selected') === 'true'
        });
    });

    // Checkboxes and radio buttons (including custom)
    document.querySelectorAll('[role="checkbox"], [role="radio"], .rc-tree-checkbox, [type="checkbox"], [type="radio"]').forEach(el => {
        components.push({
            type: el.getAttribute('role') || el.type || 'checkbox',
            selector: bestSelector(el),
            label: el.getAttribute('aria-label') || el.closest('label')?.textContent?.trim()?.slice(0, 50) || '',
            checked: el.checked || el.getAttribute('aria-checked') === 'true'
        });
    });

    // Tree components (rc-tree, react-checkbox-tree)
    document.querySelectorAll('[role="tree"]').forEach(el => {
        const items = el.querySelectorAll('[role="treeitem"]');
        components.push({
            type: 'tree',
            selector: bestSelector(el),
            treeClass: el.className,
            itemCount: items.length,
            items: Array.from(items).slice(0, 20).map(item => ({
                text: item.textContent?.trim()?.slice(0, 50),
                expanded: item.getAttribute('aria-expanded')
            }))
        });
    });

    // Drag and drop zones
    document.querySelectorAll('[draggable="true"], .ui-draggable, [class*="drag"], [class*="drop"]').forEach(el => {
        if (el.id || el.className.includes('drag') || el.className.includes('drop')) {
            components.push({
                type: 'draggable',
                selector: bestSelector(el),
                id: el.id,
                text: (el.innerText || '').trim().slice(0, 30)
            });
        }
    });

    // React-select / custom dropdowns
    document.querySelectorAll('[class*="select__control"], [class*="-control"], .css-yk16xz-control').forEach(el => {
        components.push({
            type: 'react-select',
            selector: bestSelector(el),
            placeholder: el.querySelector('[class*="placeholder"]')?.textContent?.trim() || ''
        });
    });

    // Accordions
    document.querySelectorAll('.accordion-item, .card-header[data-toggle], .accordion-button').forEach(el => {
        components.push({
            type: 'accordion',
            selector: bestSelector(el),
            text: (el.innerText || '').trim().slice(0, 50),
            expanded: el.getAttribute('aria-expanded')
        });
    });

    // Progress bars
    document.querySelectorAll('[role="progressbar"], .progress-bar').forEach(el => {
        components.push({
            type: 'progressbar',
            selector: bestSelector(el),
            value: el.getAttribute('aria-valuenow'),
            max: el.getAttribute('aria-valuemax')
        });
    });

    // Sliders / range inputs
    document.querySelectorAll('input[type="range"]').forEach(el => {
        components.push({
            type: 'slider',
            selector: bestSelector(el),
            min: el.min, max: el.max, value: el.value
        });
    });

    // Modal dialogs
    document.querySelectorAll('.modal, [role="dialog"]').forEach(el => {
        components.push({
            type: 'modal',
            selector: bestSelector(el),
            id: el.id,
            visible: el.classList.contains('show') || el.style.display !== 'none'
        });
    });

    // All elements with IDs (compact list for reference)
    const idElements = [...document.querySelectorAll('[id]')]
        .filter(el => el.offsetParent !== null || el.getAttribute('aria-hidden') !== 'true')
        .map(el => ({ id: el.id, tag: el.tagName.toLowerCase(), class: el.className?.toString()?.slice(0, 60) || '' }))
        .slice(0, 100);

    return {
        title:       document.title,
        url:         location.href,
        inputs,
        buttons,
        errors,
        links,
        forms_count: document.querySelectorAll('form').length,
        components,
        idElements
    };
}"""


# ---------------------------------------------------------------------------
# 단일 async 진입점 — 브라우저 1회만 생성
# ---------------------------------------------------------------------------
async def analyze_all(main_url: str, sub_urls: list[str],
                      force_refresh: bool = False) -> tuple[dict, dict]:
    """메인 URL + 서브 URL을 단일 브라우저에서 분석.

    Returns: (main_dom, {sub_url: sub_dom, ...})
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)

        # ── 메인 URL: networkidle (품질 우선) ──
        main_dom = None
        if not force_refresh:
            main_dom = get_cached_dom(main_url)
            if main_dom:
                print(f"[01] 캐시 사용: {main_url}")

        if main_dom is None:
            page = await browser.new_page()
            try:
                await page.goto(main_url, wait_until="networkidle", timeout=30000)
                main_dom = await page.evaluate(DOM_EXTRACT_JS)
                save_dom_cache(main_url, main_dom)
            except Exception as e:
                return {"error": str(e), "url": main_url}, {}
            finally:
                await page.close()

        # ── 서브 URL: load + 500ms (속도 우선) ──
        sub_doms = {}
        uncached = []
        for url in sub_urls:
            if not force_refresh:
                cached = get_cached_dom(url)
                if cached:
                    print(f"[01] 서브페이지 캐시 사용: {url}")
                    sub_doms[url] = cached
                    continue
            uncached.append(url)

        if uncached:
            print(f"[01] 서브페이지 {len(uncached)}개 병렬 분석 중...")
            semaphore = asyncio.Semaphore(8)

            async def _analyze_sub(url):
                async with semaphore:
                    page = await browser.new_page()
                    try:
                        await page.goto(url, wait_until="load", timeout=15000)
                        await page.wait_for_timeout(500)
                        dom = await page.evaluate(DOM_EXTRACT_JS)
                        save_dom_cache(url, dom)
                        sub_doms[url] = dom
                    except Exception as e:
                        print(f"     경고: {url} 접근 실패 — {e}")
                    finally:
                        await page.close()

            await asyncio.gather(*[_analyze_sub(u) for u in uncached])

        await browser.close()
        return main_dom, sub_doms


def url_cache_key(url: str) -> str:
    """URL을 해시해 캐시 파일명으로 사용."""
    return hashlib.md5(url.encode()).hexdigest()


def extract_subpage_urls(test_cases: list, base_url: str) -> list:
    """테스트 케이스의 precondition과 steps에서 고유 서브페이지 URL을 추출."""
    urls = set()
    for tc in test_cases:
        # precondition에서 URL 추출
        precondition = tc.get("precondition", "")
        found = re.findall(r'https?://[^\s,)]+', precondition)
        for u in found:
            u = u.rstrip(".")
            if u != base_url and u.rstrip("/") != base_url.rstrip("/"):
                urls.add(u)

        # steps 리스트에서 URL 추출
        steps = tc.get("steps", [])
        if isinstance(steps, list):
            for step in steps:
                step_text = step if isinstance(step, str) else str(step)
                found = re.findall(r'https?://[^\s,)]+', step_text)
                for u in found:
                    u = u.rstrip(".")
                    if u != base_url and u.rstrip("/") != base_url.rstrip("/"):
                        urls.add(u)

    return sorted(urls)


def main():
    state_path = PIPELINE_STATE
    if not state_path.exists():
        print("[오류] state/pipeline.json 없음. 먼저 run_qa.py를 실행하세요.")
        sys.exit(1)

    force_refresh = "--force-refresh" in sys.argv

    state = read_state(state_path)
    url = state["url"]

    print(f"[01] 페이지 분석 중: {url}")

    # 서브페이지 URL 추출
    test_cases = state.get("test_cases", [])
    sub_urls = extract_subpage_urls(test_cases, url)

    # 단일 브라우저로 메인 + 서브 모두 분석
    dom, sub_doms = asyncio.run(analyze_all(url, sub_urls, force_refresh))

    if "error" in dom:
        print(f"[오류] 페이지 접근 실패: {dom['error']}")
        sys.exit(1)

    # pipeline.json에는 캐시 키만 저장 (경량 참조)
    state["dom_info"] = dom
    state["dom_cache_key"] = url_cache_key(url)
    state["step"] = "analyzed"

    if sub_doms:
        # pipeline.json에는 URL→캐시키 매핑만 저장 (경량화)
        state["sub_dom_keys"] = {
            url: url_cache_key(url) for url in sub_doms
        }
        print(f"[01] 서브페이지 {len(sub_doms)}개 분석 완료")

    write_state(state_path, state)

    print(f"[01] 완료 ─ 제목: {dom.get('title','')}")
    print(f"       입력 필드: {len(dom.get('inputs', []))}개")
    print(f"       버튼:      {len(dom.get('buttons', []))}개")
    print(f"       에러 영역: {len(dom.get('errors', []))}개")
    print(f"       컴포넌트:  {len(dom.get('components', []))}개")
    print(f"       ID 요소:   {len(dom.get('idElements', []))}개")
    print()
    print("[다음] Claude Code가 dom_info를 읽고 테스트 전략(plan)을 수립합니다.")


if __name__ == "__main__":
    main()
