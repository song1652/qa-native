# Plan 심의 프롬프트 (02a_dialog.py 후 사용)

> 이 파일은 심의 Agent에 대한 행동 지침이다.
> `{ctx.*}` 참조는 DELIBERATION_CONTEXT JSON의 해당 키를 의미한다.

아래 컨텍스트를 바탕으로 사수(Senior QA Lead)와 부사수(Junior QA Engineer) 두 관점을
내부적으로 시뮬레이션하여 테스트 plan을 확정하라.

team_charter: {ctx.team_charter}
senior_role: {ctx.senior_role}
junior_role: {ctx.junior_role}
lessons_learned: {ctx.lessons_learned}
dom_info: {ctx.dom_info}
test_cases: {ctx.test_cases}

출력 형식:
1. state/pipeline.json에 plan 저장, step = "planned"

plan 각 항목 JSON 스키마:
```json
{
  "case_name": "tc_{번호}_{english_snake_case}",
  "case_type": "structured | natural",
  "description": "테스트 목적을 구체적으로 기술 (모호한 표현 금지)",
  "steps": [
    {"action": "goto|fill|click|hover|select|wait|evaluate", "selector": "#id 또는 dom_info 기반 셀렉터", "value": "test_data 참조 또는 리터럴"}
  ],
  "assertion": {
    "type": "url_contains|element_visible|text_contains|element_count|class_contains",
    "expected": "기대 결과 (외부 사이트 메시지 하드코딩 금지)"
  }
}
```
- structured 케이스: precondition/steps/expected 직접 반영
- natural 케이스: dom_info 기반 steps/assertion 자동 추론

## Few-shot 예시 (참조용)

good plan 예시: `prompts/examples/plan_good.json` — 셀렉터를 dom_info에서 확인, test_data 참조, 영문 snake_case
bad plan 예시: `prompts/examples/plan_bad.json` — 셀렉터 추측, 하드코딩, 한글 함수명, 모호한 description

## 핵심 규칙 (CLAUDE.md 발췌)
- 테스트 함수명: 반드시 영문 snake_case `test_{english_snake_case}` (한글 제목도 영어 번역)
- tc_*.md 1개 = 테스트 파일 1개 = 테스트 함수 1개
- 테스트 데이터 하드코딩 금지 -> config/test_data.json 참조
- lessons_learned를 반드시 먼저 확인하고 같은 실수 반복 금지
- Playwright 코드 규칙: `.claude/skills/playwright-best-practices/SKILL.md` 참조
