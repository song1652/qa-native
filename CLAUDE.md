# QA Automation — Claude Code Native

> **독자**: Claude Code — 파이프라인 전체 실행 지침. 변경 시 즉시 업데이트.

## 개요
API 호출 없이 Claude Code 자체가 LLM 역할을 수행하는 QA 자동화 시스템.
모든 단계 결과는 `state/pipeline.json`에 누적되며, Claude Code가 순서대로 직접 실행한다.

---

## 절대 규칙
- `anthropic`, `langchain`, `openai` 등 외부 LLM SDK import 절대 금지
- API 키 사용 금지
- 모든 단계 결과는 반드시 state/pipeline.json에 저장 후 다음 단계 진행
- 코드 생성은 Claude Code가 직접 파일로 작성 (문자열 출력 후 저장 아님)
- **lessons_learned 필수 참조**: 코드 작성·리뷰·힐링 전 `agents/lessons_learned.md`를 반드시 확인하고, 같은 실수를 반복하지 않는다
- **테스트 함수명은 반드시 영문 snake_case**: 케이스 제목이 한글이어도 의미를 영어로 번역해 `test_{english_snake_case}` 형식으로 작성
  - 예) "정상 로그인 성공" → `test_login_success`
  - 예) "잘못된 비밀번호 입력 후 에러 메시지 표시" → `test_wrong_password_shows_error_message`
- **테스트 파일은 자체 완결**: 공유 헬퍼 파일(helpers.py 등) 생성 금지. 각 테스트 파일이 필요한 import·상수·유틸을 직접 포함해야 한다
  - BASE_URL, LOGIN_URL → 파일 상단에 직접 선언
  - 테스트 데이터 → `config/test_data.json`을 파일 내에서 직접 읽기
  - 로그인 등 공통 동작 → 각 파일 내 인라인 구현
- **tc_*.md 1개 = 테스트 파일 1개 = 테스트 함수 1개**: 파일당 테스트 함수를 2개 이상 만들지 않는다

---

## 설정 파일

### URL 관리 — `config/pages.json`
형식: `{ "페이지명": "https://..." }` — 키는 testcases/ 하위 폴더명과 일치.
- `run_qa_parallel.py` 실행 시 `--targets` 생략 가능 → testcases/ 폴더 자동 스캔 + pages.json URL 자동 조회
- URL이 없는 폴더는 자동으로 건너뜀

### 테스트 데이터 — `config/test_data.json`
- 키 = pages.json의 페이지명과 일치
- 테스트케이스 frontmatter의 `data_key`가 서브키를 참조 (예: `data_key: valid_user`)
- 테스트 코드에서 하드코딩 금지 — 반드시 이 파일에서 읽어 사용

### 테스트케이스 형식
- YAML frontmatter + Markdown 본문으로 작성
- frontmatter 필수 필드: `id`, `data_key`, `priority`, `tags`, `type`
- `data_key`: test_data.json의 서브키와 1:1 매핑 (입력 불필요 시 `null`)
- Steps 입력값: `test_data[{data_key}].{속성}` 형식 참조 (하드코딩 금지)
- `parse_cases.py`가 frontmatter를 자동 파싱하여 id/data_key/priority/tags를 케이스에 포함

---

## 실행 원칙 (속도 최적화)
- **병렬 우선**: 독립적인 작업은 반드시 동시에 실행한다. 순서 의존성이 없는 한 절대 순차 실행하지 않는다.
- **심의 Agent 1회 호출**: 사수/부사수 역할을 별도 subagent로 분리하지 않는다. 단일 심의 agent가 두 관점을 내부 시뮬레이션해 결론을 낸다.
- **컨텍스트 주입**: `02a/03a/06a_dialog.py`가 출력하는 `DELIBERATION_CONTEXT` JSON을 심의 agent 프롬프트에 직접 포함한다. agent가 추가로 파일을 읽지 않도록 한다.

---

## 공통: 힐링 패치 기준

모든 파이프라인(단일/병렬)에서 힐링 시 동일 기준 적용:

| 오류 유형 | 판별 키워드 | 패치 방법 |
|-----------|------------|-----------|
| Locator | `strict mode violation`, `Element not found` | dom_info 셀렉터와 대조해 수정 |
| Assertion | `Expected ... to contain` | 실제 페이지 텍스트를 기댓값으로 수정 |
| Timeout | `Timeout` | `page.wait_for_selector()` 추가 또는 `expect(..., timeout=10000)` 조정 |
| URL | `goto`, `navigation` | BASE_URL 또는 goto 인자 수정 |

**[필수] 힐링 완료 체크리스트** (하나라도 빠지면 힐링 미완료):
1. 코드 패치 적용
2. `agents/lessons_learned.md`에 아래 형식으로 기록 (`99_merge.py`가 `[힐링 대기]` 스텁을 생성하면 `[힐링]`으로 바꾸고 수정/재발 방지 기입):
   ```
   ### [힐링] {날짜} — {파일명}
   - **문제**: {traceback 요약}
   - **수정**: {적용한 패치 내용}
   - **재발 방지**: {동일 실수 방지 규칙}
   ```
3. 재실행으로 통과 확인

### MCP 시각 검증 (힐링 시 선택 사용)

traceback만으로 원인이 불명확한 Locator/Assertion/Timeout 오류에만 사용한다.
heal_context의 각 failure에 `screenshot` 경로가 포함되어 있으면 활용 가능.

1. **스크린샷 확인**: Read tool로 `heal_context.failures[].screenshot.path` 파일 열기 → 실패 시점 화면 확인
2. **실제 페이지 탐색** (필요 시만):
   - `Playwright_navigate` → heal_context의 URL로 접속
   - `playwright_get_visible_html` → 현재 페이지 DOM 구조 확인
   - `playwright_get_visible_text` → 현재 페이지 텍스트 확인
3. **셀렉터 검증** (필요 시만):
   - `Playwright_evaluate` → `document.querySelector('셀렉터')` 로 셀렉터 존재 확인
4. **패치 적용**: 시각 검증 결과를 바탕으로 테스트 코드 수정

**주의사항**:
- MCP 도구는 힐링 경로에서만 사용 (정상 실행 시 사용 금지 → 비용 절감)
- MCP 브라우저와 pytest 브라우저는 별개 세션이므로 쿠키/상태가 공유되지 않는다
- 로그인 등 전제조건이 필요한 페이지는 DOM/텍스트 확인에 그친다

---

## 단일 파이프라인 (단일 URL)

### 실행 순서

```
01_analyze.py   → DOM 추출 (LLM 없음)

02a_dialog.py   → 컨텍스트 수집·출력 (파일 병렬 읽기, LLM 없음)
[심의 Agent 1회] → DELIBERATION_CONTEXT 주입 → 사수/부사수 내부 시뮬레이션
                   → plan 확정 → state/pipeline.json 저장 (step="planned")

[병렬 실행]
  02_generate.py  → 코드 뼈대 생성
  ↓ (병렬 완료 후)
  Claude Code가 코드 완성 → tests/generated/test_generated.py

03_lint.py      → flake8 검사 (LLM 없음)

03a_dialog.py   → 컨텍스트 수집·출력 (파일 병렬 읽기, LLM 없음)
[심의 Agent 1회] → DELIBERATION_CONTEXT 주입 → 코드 + lint 내부 심의
                   → 수정 확정 → state/pipeline.json 저장 (step="reviewed")

04_approve.py   → 요약 출력 후 y/n 대기
05_execute.py   → pytest 실행 → state/pipeline.json에 결과 저장
                   (매 실행 전 tests/screenshots/ 초기화)

06_heal.py      → 실패 분석 → heal_context 저장 (LLM 없음)

06a_dialog.py   → 컨텍스트 수집·출력 (파일 병렬 읽기, LLM 없음)
[심의 Agent 1회] → DELIBERATION_CONTEXT 주입 → 트레이스백 진단·패치 내부 심의
                   → 패치 확정 → test_generated.py 직접 수정
                   → 05_execute.py --no-report 재실행 (최대 3회)
                   → 힐링 완료 후 05_execute.py (리포트 포함) 최종 실행
```

### Claude Code 실행 방법

사용자가 아래처럼 요청하면 파이프라인을 순서대로 실행한다:

```
run_qa.py를 실행해줘
URL: https://example.com/login
테스트 케이스: testcases/login/
```

> **참고**: `--cases`에 폴더 경로를 지정하면 `parse_cases.py`가 폴더 내 `tc_*.md` 파일을 모두 읽어 자동 병합한다. 단일 파일 지정도 가능.

Claude Code는:

**1.** `python scripts/01_analyze.py` 실행

**2.** `python scripts/02a_dialog.py` 실행
   출력에서 `DELIBERATION_CONTEXT_START ~ END` 사이의 JSON을 추출한다.
   **[심의 Agent 1회 호출]** — `prompts/plan_deliberation.md` 템플릿 참조.
   DELIBERATION_CONTEXT JSON의 각 필드를 템플릿의 `{ctx.*}` 자리에 대입해 agent 실행.

**3.** `python scripts/02_generate.py` 실행
   `tests/generated/{group}/` 디렉토리에 케이스별 scaffold 파일이 생성됨.
   각 scaffold 파일을 plan 기반으로 개별 완성:
   - tc_*.md 1개 = 테스트 파일 1개 = 테스트 함수 1개
   - 각 파일은 자체 완결 (import, BASE_URL, TEST_DATA_PATH 직접 포함)
   - TEST_DATA_PATH: `Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"` (.parent 4번)
   - 함수명은 반드시 영문 snake_case: test_{english_snake_case} (한글 제목이어도 영어로 번역)

**4.** `python scripts/03_lint.py` 실행

**5.** `python scripts/03a_dialog.py` 실행
   출력에서 DELIBERATION_CONTEXT JSON 추출.
   **[심의 Agent 1회 호출]** — `prompts/review_deliberation.md` 템플릿 참조.
   DELIBERATION_CONTEXT JSON의 각 필드를 템플릿의 `{ctx.*}` 자리에 대입해 agent 실행.

**6.** `python scripts/04_approve.py` 실행 → 사용자에게 y/n 요청
   반려 시 rejection_reason 저장 → 3번으로 돌아가 코드 재작성

**7.** 승인 시 `python scripts/05_execute.py` 실행

**8.** `python scripts/06_heal.py` 실행
   - 종료코드 0: 전체 통과 → `python scripts/05_execute.py` 실행 (리포트 생성) → 완료
   - 종료코드 1: heal_context 저장됨 →
     `python scripts/06a_dialog.py` 실행
     출력에서 DELIBERATION_CONTEXT JSON 추출.
     **[심의 Agent 1회 호출]** — `prompts/heal_deliberation.md` 템플릿 참조.
     DELIBERATION_CONTEXT JSON의 각 필드를 템플릿의 `{ctx.*}` 자리에 대입해 agent 실행.
     → `python scripts/05_execute.py --no-report` 로 재실행 (리포트 생성 안 함)
     → 8번으로 돌아가 반복
   - 종료코드 2: 최대 힐링 횟수 초과 → `python scripts/05_execute.py` 실행 (최종 리포트 생성) → 사용자에게 수동 수정 요청

> **리포트/스크린샷 정책**: 05_execute.py는 매 실행 전 `tests/screenshots/`를 초기화한다. 힐링 중간 실행은 `--no-report`로 리포트 생성을 건너뛴다. 최종 실행(전체 통과 또는 힐링 초과)에서만 리포트를 생성하므로, 리포트와 스크린샷 모두 마지막 실행 결과만 남는다.

대시보드 실행 (선택): `python agents/dashboard/serve.py`

---

## 병렬 파이프라인 (다중 URL)

여러 URL/케이스 폴더를 동시에 테스트할 때 사용한다.
subagent가 코드 생성만 병렬로 수행하고, pytest는 일괄 실행한다.

### 실행 순서

```
python run_qa_parallel.py
  → testcases/ 폴더 스캔 + config/pages.json URL 조회
  → URL별 DOM 분석 (캐시, 동일 URL 1회만)
  → tc_*.md 파일별 subagent 컨텍스트 생성
  → PARALLEL_SUBAGENT_CONTEXTS 출력
```

Claude Code는 출력의 `PARALLEL_SUBAGENT_CONTEXTS_START ~ END` 사이의 JSON을 읽고
각 항목을 Agent tool로 **동시에** 실행한다.

### Subagent 지시 형식

각 subagent는 `prompts/parallel_subagent.md` 템플릿을 참조하여 테스트 코드를 직접 생성한다.
**스크립트 실행 없이**, 컨텍스트만으로 코드를 작성하고 output_path에 저장한다.
PARALLEL_SUBAGENT_CONTEXTS JSON의 각 필드를 템플릿의 `{ctx.*}` 자리에 대입해 agent 실행.

### 전체 완료 후

모든 subagent 완료 후:
```
python parallel/99_merge.py
  → tests/generated/ 에서 pytest 일괄 실행
  → 실패 시 state/heal_context.json → 힐링 루프 (최대 3회)
  → tests/reports/parallel_index_{ts}.html 생성
```

**힐링 루프 (99_merge.py 실패 시):**
- `state/heal_context.json`이 생성되면 Claude Code가 힐링을 수행한다
- 공통 힐링 패치 기준 + 힐링 완료 체크리스트 참조
- heal_context.json의 각 failure에 screenshot 경로 포함 → Read tool로 시각 확인 가능
- traceback만으로 원인 불명확 시 MCP 시각 검증 절차 참조
- 패치 후 `python parallel/99_merge.py` 재실행 (최대 3회, heal_count 자동 누적)
- 3회 초과 시 수동 수정 요청

---

## 팀 자유 토론 파이프라인

사용자가 `run_team.py`를 실행하면 아래 순서로 진행한다.
어떤 주제든 사수/부사수가 토론하고, 사용자가 결론을 최종 승인한다.

### 실행 순서

```
python run_team.py --topic "주제"
  → state/discuss.json 초기화
```

**1.** `python scripts/team_discuss.py` 실행
   출력에서 `DELIBERATION_CONTEXT_START ~ END` 사이의 JSON 추출.
   **[심의 Agent — 멀티라운드 티키타카 진행]** — `prompts/team_discussion.md` 템플릿 참조.
   DELIBERATION_CONTEXT JSON의 각 필드를 템플릿의 `{ctx.*}` 자리에 대입해 agent 실행.

   > **핵심 규칙: 발언 1개 작성 → 즉시 dialog.json 저장 → 다음 발언 작성 → 즉시 저장 → 반복**
   > 배치 저장 금지. 대시보드가 3초마다 폴링하므로 한 발언씩 저장해야 실시간으로 보인다.

   결론 저장:
   state/discuss.json → `{ "step": "discussed", "conclusion": "결론 (마크다운)" }`

**2.** 심의 완료 후 사용자에게 알림:
   "토론이 완료됐어요. 대시보드에서 결론을 확인하고 승인/반려해주세요."
   (대시보드 http://localhost:8765 → 해당 토론 세션 하단에 승인/반려 버튼이 표시됩니다)
   - 승인 시: 서버가 `agents/team_notes.md` 저장 + `pending_impl.json` 생성
     → 스케줄러(2분 내)가 `pending_impl.json` 감지 → Claude가 항목 자동 구현
     → 구현 완료 후 `pending_impl.json` 삭제, `team_notes.md`·`state/discuss.json` 초기화
   - 반려 시: rejection_reason 저장, state/discuss.json step = "rejected" → 재토론 요청

---

## state/pipeline.json 구조
```json
{
  "url": "",
  "test_cases": [],
  "step": "init | analyzed | planned | generated | reviewed | approved | done | heal_needed | heal_failed",
  "dom_info": {},
  "plan": [],
  "cases_path": "testcases/{group}/",
  "group_dir": "{group}",
  "generated_file_path": "tests/generated/{group}/",
  "generated_files": [],
  "lint_result": {},
  "review_summary": "",
  "approval_status": "approved | rejected",
  "rejection_reason": "",
  "rejection_count": 0,
  "execution_result": {},
  "heal_count": 0,
  "heal_context": {
    "heal_count": 0,
    "failure_count": 0,
    "failures": [
      { "test_id": "", "test_name": "", "traceback": "" }
    ],
    "raw_tail": "",
    "analyzed_at": ""
  }
}
```

---

## 디렉토리
```
scripts/            단계별 실행 스크립트 (LLM 없음, 순수 Python)
  01_analyze.py     DOM 추출
  02_generate.py    코드 뼈대 생성
  02a_dialog.py     Plan 대화 세션 초기화
  03_lint.py        flake8 검사
  03a_dialog.py     코드 리뷰 대화 세션 초기화
  04_approve.py     승인/반려
  05_execute.py     pytest 실행
  06_heal.py        실패 분석
  06a_dialog.py     힐링 대화 세션 초기화
  team_discuss.py   팀 토론 초기화
  parse_cases.py    tc_*.md 파싱
  _python.py        .venv 경로 자동 감지
  _paths.py         중앙 경로 상수 (state/, logs/)
  team_approve.py   팀 토론 승인 (터미널용)
  sync_test_data.py test_data.json 동기화
  check_pending_*.py  훅 스크립트 (approve/discuss/impl/parallel/pipeline)

agents/             사수-부사수 에이전트 시스템
  team_charter.md   팀 헌장 (협업 규칙, 역할 정의)
  IDENTITY.md       사수/부사수 페르소나 (말투, 성격, 대화 예시)
  SOUL.md           팀 원칙과 가치관
  dialog.json       팀 토론 대화 로그 전용 (QA 파이프라인 심의 기록 안 함)
  lessons_learned.md  실수 패턴 누적 (힐링·코드리뷰 시 자동 추가)
  team_notes.md     승인된 팀 결정사항
  roles/
    senior.md       사수 행동 지침 (상세)
    junior.md       부사수 행동 지침 (상세)
  dashboard/
    index.html      팀 토론 모니터링·승인 대시보드 UI
    serve.py        대시보드 로컬 서버 (python agents/dashboard/serve.py)

prompts/            심의 Agent 프롬프트 템플릿 (CLAUDE.md에서 분리)
  plan_deliberation.md      02a 심의 — plan 수립
  review_deliberation.md    03a 심의 — 코드 리뷰
  heal_deliberation.md      06a 심의 — 힐링 패치
  parallel_subagent.md      병렬 subagent 코드 생성
  team_discussion.md        팀 토론 멀티라운드

state/              상태 파일 (런타임 생성)
  pipeline.json     단일 파이프라인 상태
  discuss.json      팀 토론 상태
  parallel.json     병렬 파이프라인 상태
  quick.json        빠른 실행 상태
  heal_context.json 힐링 루프용 traceback (실패 시 생성)

logs/               실행 로그 (런타임 생성)
  run_qa.txt        단일 파이프라인 로그
  run_parallel.txt  병렬 파이프라인 로그
  merge.txt         99_merge.py 로그
  quick_run.txt     빠른 실행 로그

parallel/           병렬 파이프라인 스크립트
  99_merge.py       pytest 실행 + 통합 리포트 + 힐링 루프

tests/generated/    Claude Code가 작성한 테스트 코드 (서브폴더별 __init__.py 필수)
tests/reports/      HTML 리포트
tests/screenshots/  실패 시 스크린샷

testcases/          케이스 파일 (tc_*.md) — 그룹별 서브폴더로 관리
config/
  pages.json        페이지명 → URL 매핑 (중앙 URL 레지스트리)
  test_data.json    테스트 입력값 (계정, 폼 데이터)

knowledge/          QA 지식 베이스
  qa-checklist.md   스모크 항목 + Playwright 작성 체크리스트
  team-rules.md     팀 내규 (TC ID, 우선순위, 소통, 리뷰, 이슈 관리)
  workflow-guide.md 파이프라인 워크플로우 가이드

templates/          문서 템플릿
  tc-template.md    테스트케이스 작성 템플릿
  report-template.md 테스트 리포트 템플릿
  issue-template.md  이슈(버그) 리포트 템플릿

reports/issues/     이슈 추적 파일 (ISSUE-{날짜}-{번호}.md)
run_qa.py           단일 파이프라인 진입점
run_qa_parallel.py  병렬 파이프라인 진입점
run_team.py         팀 토론 진입점
doc/                내부 문서 (PROJECT_OVERVIEW, SCRIPTS_GUIDE, TEST_CASE_GUIDE)
```
