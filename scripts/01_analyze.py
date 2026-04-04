"""
Step 1 — 페이지 DOM 분석
LLM 없음. Playwright로 직접 DOM 추출.
결과를 state.json의 dom_info에 저장.

Claude Code는 이 스크립트 실행 후
dom_info를 읽고 테스트 전략(plan)을 직접 수립해서 state.json에 저장한다.
"""
import json
import asyncio
import hashlib
import sys
from pathlib import Path
from playwright.async_api import async_playwright
from _paths import PIPELINE_STATE, DOM_CACHE_DIR, read_state, write_state


async def analyze(url: str) -> dict:
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        try:
            await page.goto(url, wait_until="networkidle", timeout=30000)
        except Exception as e:
            await browser.close()
            return {"error": str(e), "url": url}

        # DOM 구조 추출 — 순수 JS, LLM 불필요
        dom = await page.evaluate("""() => {
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

            return {
                title:       document.title,
                url:         location.href,
                inputs,
                buttons,
                errors,
                links,
                forms_count: document.querySelectorAll('form').length
            };
        }""")

        await browser.close()
        return dom


def url_cache_key(url: str) -> str:
    """URL을 해시해 캐시 파일명으로 사용."""
    return hashlib.md5(url.encode()).hexdigest()


def get_cached_dom(url: str) -> dict | None:
    """캐시된 DOM 분석 결과가 있으면 반환."""
    cache_file = DOM_CACHE_DIR / f"{url_cache_key(url)}.json"
    if cache_file.exists():
        try:
            return json.loads(cache_file.read_text(encoding="utf-8"))
        except Exception:
            pass
    return None


def save_dom_cache(url: str, dom: dict):
    """DOM 분석 결과를 캐시에 저장."""
    DOM_CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cache_file = DOM_CACHE_DIR / f"{url_cache_key(url)}.json"
    cache_file.write_text(json.dumps(dom, ensure_ascii=False, indent=2), encoding="utf-8")


def extract_subpage_urls(test_cases: list, base_url: str) -> list[str]:
    """테스트 케이스의 precondition에서 고유 서브페이지 URL을 추출."""
    urls = set()
    for tc in test_cases:
        precondition = tc.get("precondition", "")
        # precondition에서 URL 추출 (https://... 패턴)
        import re
        found = re.findall(r'https?://[^\s,)]+', precondition)
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

    state = read_state(state_path)
    url = state["url"]

    # 메인 URL 분석
    print(f"[01] 페이지 분석 중: {url}")
    dom = get_cached_dom(url)
    if dom:
        print(f"[01] 캐시 사용: {url}")
    else:
        dom = asyncio.run(analyze(url))
        if "error" in dom:
            print(f"[오류] 페이지 접근 실패: {dom['error']}")
            sys.exit(1)
        save_dom_cache(url, dom)

    # dom_info는 캐시에 저장되므로, pipeline.json에는 경량 참조만 저장
    state["dom_info"] = dom
    state["dom_cache_key"] = url_cache_key(url)
    state["step"] = "analyzed"

    # 서브페이지 DOM 분석 (precondition URL)
    test_cases = state.get("test_cases", [])
    sub_urls = extract_subpage_urls(test_cases, url)
    if sub_urls:
        sub_doms = {}
        for sub_url in sub_urls:
            cached = get_cached_dom(sub_url)
            if cached:
                print(f"[01] 서브페이지 캐시 사용: {sub_url}")
                sub_doms[sub_url] = cached
            else:
                print(f"[01] 서브페이지 분석 중: {sub_url}")
                sub_dom = asyncio.run(analyze(sub_url))
                if "error" not in sub_dom:
                    save_dom_cache(sub_url, sub_dom)
                    sub_doms[sub_url] = sub_dom
                else:
                    print(f"     경고: {sub_url} 접근 실패 — {sub_dom['error']}")
        if sub_doms:
            state["sub_dom_info"] = sub_doms
            print(f"[01] 서브페이지 {len(sub_doms)}개 분석 완료")

    write_state(state_path, state)

    print(f"[01] 완료 ─ 제목: {dom.get('title','')}")
    print(f"       입력 필드: {len(dom.get('inputs', []))}개")
    print(f"       버튼:      {len(dom.get('buttons', []))}개")
    print(f"       에러 영역: {len(dom.get('errors', []))}개")
    print()
    print("[다음] Claude Code가 dom_info를 읽고 테스트 전략(plan)을 수립합니다.")


if __name__ == "__main__":
    main()
