# QA Automation — Claude Code Native

> **독자**: Claude Code — 파이프라인 전체 실행 지침.
> 상세: [HEALING_GUIDE](doc/HEALING_GUIDE.md), [TEAM_DISCUSSION](doc/TEAM_DISCUSSION.md), [PIPELINE_STATE](doc/PIPELINE_STATE.md), [DIRECTORY](doc/DIRECTORY.md)

## 행동 원칙
- 이미 읽은 파일은 재읽기 금지
- 독립적 도구 호출은 반드시 병렬 실행
- 완료 보고 시 이미 설명한 내용 반복 금지

API 호출 없이 Claude Code 자체가 LLM 역할을 수행하는 QA 자동화 시스템.
모든 단계 결과는 `state/pipeline.json`에 누적되며, Claude Code가 순서대로 직접 실행한다.

## 절대 규칙
- `anthropic`, `langchain`, `openai` 등 외부 LLM SDK import 절대 금지. API 키 사용 금지
- 모든 단계 결과는 반드시 state/pipeline.json에 저장 후 다음 단계 진행
- 코드 생성은 Claude Code가 직접 파일로 작성 (문자열 출력 후 저장 아님)
- **lessons_learned 필수 참조**: 코드 작성·리뷰·힐링 전 `agents/lessons_learned.md` 확인
- **테스트 함수명**: 반드시 영문 snake_case `test_{english_snake_case}` (한글 제목도 영어로 번역)
- **테스트 파일은 자체 완결**: 공유 헬퍼 파일 생성 금지. BASE_URL·import·상수를 각 파일에 직접 포함
- **tc_*.md 1개 = 테스트 파일 1개 = 테스트 함수 1개**
- **파일명 규칙 (단일/병렬 공통)**: `tc_{번호}_{english_snake_case}.py` (예: `tc_01_login_success.py`)

## 설정 파일

| 파일 | 용도 |
|------|------|
| `config/pages.json` | `{ "페이지명": "URL" }` — 키는 testcases/ 하위 폴더명과 일치 |
| `config/test_data.json` | 키 = pages.json 페이지명. frontmatter `data_key`가 서브키 참조. 하드코딩 금지 |

**테스트케이스**: YAML frontmatter (`id`, `data_key`, `priority`, `tags`, `type`) + Markdown 본문.
`parse_cases.py`가 자동 파싱. 입력값은 `test_data[{data_key}].{속성}` 형식 참조.

## 실행 원칙
- **병렬 우선**: 독립 작업은 반드시 동시 실행
- **심의 Agent 1회 호출**: 사수/부사수를 단일 agent가 내부 시뮬레이션
- **컨텍스트 주입**: `*_dialog.py`가 출력하는 `DELIBERATION_CONTEXT` JSON을 심의 agent 프롬프트에 직접 포함

## 스킬 프레임워크

`.claude/skills/`에 정적 베스트프랙티스를 SKILL.md 표준으로 관리. 자체 로더/엔진 없이 공식 표준 그대로 활용.

| 스킬 | 경로 | 용도 |
|------|------|------|
| Playwright Best Practices | `.claude/skills/playwright-best-practices/SKILL.md` | 테스트 코드 작성 시 참조 |
| Heal Patterns | `.claude/skills/heal-patterns/SKILL.md` | 힐링 패치 전략 참조 |

동적 빈도 데이터는 `state/heal_stats.json`에 기록되며, `06a_dialog.py`가 Top 5 빈출 패턴을 DELIBERATION_CONTEXT에 자동 주입.

## 힐링

힐링 완료 필수: (1) 코드 패치 (2) lessons_learned.md에 한 줄 패턴 기록 (중복 시 생략) (3) 재실행 통과 확인.
오류 유형별 패치 전략 → `.claude/skills/heal-patterns/SKILL.md`. MCP 시각 검증 → [HEALING_GUIDE](doc/HEALING_GUIDE.md)

## 단일 파이프라인 (단일 URL)

```
01_analyze → 02a_dialog → [심의] → 02_generate → 03_lint → 03a_dialog → [심의] → 04_approve → 05_execute → 06_heal → [힐링 루프]
```

1. `python scripts/01_analyze.py` — DOM 추출
2. `python scripts/02a_dialog.py` → [심의] `prompts/plan_deliberation.md` + ctx
3. `python scripts/02_generate.py` — scaffold 생성 후 plan 기반 개별 완성
4. `python scripts/03_lint.py` — flake8
5. `python scripts/03a_dialog.py` → [심의] `prompts/review_deliberation.md` + ctx
6. `python scripts/04_approve.py` → 반려 시 3번으로
7. `python scripts/05_execute.py` — pytest 실행
8. `python scripts/06_heal.py` — 종료코드 0: 완료 / 1: 힐링→재실행 반복 / 2: 초과→수동 수정

> **⚠ 리포트/스크린샷 규칙 (필수)**:
> - **첫 실행 포함 모든 실행은 `--no-report`로 실행**. 리포트·스크린샷은 전체 통과 확인 후 마지막 1회만 생성.
> - 실행 순서: `05_execute.py --no-report` → `06_heal.py` → 패치 → `05_execute.py --no-report` → ... → 전체 통과 확인 → `05_execute.py` (리포트 생성)
> - 05_execute.py는 매 실행 전 tests/screenshots/ 초기화.

## 병렬 파이프라인 (다중 URL)

```
run_qa_parallel.py → testcases/ 스캔 + pages.json URL 조회 → PARALLEL_SUBAGENT_CONTEXTS 출력
```

1. `PARALLEL_SUBAGENT_CONTEXTS_START ~ END` JSON 읽기
2. 각 항목을 Agent tool로 **동시에** 실행 — `prompts/parallel_subagent.md` 참조
3. 모든 subagent 완료 후 `python parallel/99_merge.py`
4. 실패 시 힐링 루프 (최대 3회, [HEALING_GUIDE](doc/HEALING_GUIDE.md) 참조). 초과 시 수동 수정 요청

## 팀 토론

`python run_team.py --topic "주제"` → 사수/부사수 멀티라운드 토론 → 대시보드 승인/반려.
상세 → [TEAM_DISCUSSION](doc/TEAM_DISCUSSION.md)

## 참조

- state/pipeline.json 스키마 → [PIPELINE_STATE](doc/PIPELINE_STATE.md)
- 디렉토리 구조 → [DIRECTORY](doc/DIRECTORY.md)
- 스크립트 인자/옵션 상세 → [SCRIPTS_GUIDE](doc/SCRIPTS_GUIDE.md)
