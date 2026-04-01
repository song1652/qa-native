"""
Step 1 — 페이지 DOM 분석
LLM 없음. Playwright로 직접 DOM 추출.
결과를 state.json의 dom_info에 저장.

Claude Code는 이 스크립트 실행 후
dom_info를 읽고 테스트 전략(plan)을 직접 수립해서 state.json에 저장한다.
"""
import json
import asyncio
import sys
from pathlib import Path
from playwright.async_api import async_playwright
from _paths import PIPELINE_STATE


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


def main():
    state_path = PIPELINE_STATE
    if not state_path.exists():
        print("[오류] state/pipeline.json 없음. 먼저 run_qa.py를 실행하세요.")
        sys.exit(1)

    state = json.loads(state_path.read_text(encoding="utf-8"))
    url = state["url"]

    print(f"[01] 페이지 분석 중: {url}")
    dom = asyncio.run(analyze(url))

    if "error" in dom:
        print(f"[오류] 페이지 접근 실패: {dom['error']}")
        sys.exit(1)

    state["dom_info"] = dom
    state["step"] = "analyzed"
    state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"[01] 완료 ─ 제목: {dom.get('title','')}")
    print(f"       입력 필드: {len(dom.get('inputs', []))}개")
    print(f"       버튼:      {len(dom.get('buttons', []))}개")
    print(f"       에러 영역: {len(dom.get('errors', []))}개")
    print()
    print("[다음] Claude Code가 dom_info를 읽고 테스트 전략(plan)을 수립합니다.")


if __name__ == "__main__":
    main()
