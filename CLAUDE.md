# QA Automation — Claude Code Native

> **독자**: Claude Code — 파이프라인 전체 실행 지침. 변경 시 즉시 업데이트.

## 개요
API 호출 없이 Claude Code 자체가 LLM 역할을 수행하는 QA 자동화 시스템.
모든 단계 결과는 `state.json`에 누적되며, Claude Code가 순서대로 직접 실행한다.

## 절대 규칙
- `anthropic`, `langchain`, `openai` 등 외부 LLM SDK import 절대 금지
- API 키 사용 금지
- 모든 단계 결과는 반드시 state.json에 저장 후 다음 단계 진행
- 코드 생성은 Claude Code가 직접 파일로 작성 (문자열 출력 후 저장 아님)
- **테스트 함수명은 반드시 영문 snake_case**: 케이스 제목이 한글이어도 의미를 영어로 번역해 `test_{english_snake_case}` 형식으로 작성
  - 예) "정상 로그인 성공" → `test_login_success`
  - 예) "잘못된 비밀번호 입력 후 에러 메시지 표시" → `test_wrong_password_shows_error_message`

## URL 관리
URL은 `config/pages.json` 한 곳에서 관리한다:
```json
{
  "login":    "https://example.com/login",
  "home":     "https://example.com/",
  "checkout": "https://example.com/checkout"
}
```
- 키 = testcases/ 하위 폴더명
- `run_qa_parallel.py` 실행 시 `--targets` 생략 가능 → testcases/ 폴더 자동 스캔 + pages.json URL 자동 조회
- URL이 없는 폴더는 자동으로 건너뜀

## 테스트 데이터 관리
테스트 입력값(계정, 폼 데이터 등)은 `config/test_data.json` 한 곳에서 관리한다:
```json
{
  "login": {
    "valid_user": { "username": "tomsmith", "password": "SuperSecretPassword!" },
    "invalid_user": { "username": "wronguser", "password": "wrongpassword" }
  }
}
```
- 키 = pages.json의 페이지명과 일치
- 테스트 코드에서 하드코딩 금지 — 반드시 이 파일에서 읽어 사용
- DOM 추측 없이 안정적인 입력값 보장

## 실행 원칙 (속도 최적화)
- **병렬 우선**: 독립적인 작업은 반드시 동시에 실행한다. 순서 의존성이 없는 한 절대 순차 실행하지 않는다.
- **심의 Agent 1회 호출**: 사수/부사수 역할을 별도 subagent로 분리하지 않는다. 단일 심의 agent가 두 관점을 내부 시뮬레이션해 결론을 낸다.
- **컨텍스트 주입**: `02a/03a/06a_dialog.py`가 출력하는 `DELIBERATION_CONTEXT` JSON을 심의 agent 프롬프트에 직접 포함한다. agent가 추가로 파일을 읽지 않도록 한다.

---

## 단일 파이프라인 (단일 URL)

### 실행 순서

```
01_analyze.py   → DOM 추출 (LLM 없음)

02a_dialog.py   → 컨텍스트 수집·출력 (파일 병렬 읽기, LLM 없음)
[심의 Agent 1회] → DELIBERATION_CONTEXT 주입 → 사수/부사수 내부 시뮬레이션
                   → plan 확정 → state.json 저장 (step="planned")

[병렬 실행]
  02_generate.py  → 코드 뼈대 생성
  ↓ (병렬 완료 후)
  Claude Code가 코드 완성 → tests/generated/test_generated.py

03_lint.py      → flake8 검사 (LLM 없음)

03a_dialog.py   → 컨텍스트 수집·출력 (파일 병렬 읽기, LLM 없음)
[심의 Agent 1회] → DELIBERATION_CONTEXT 주입 → 코드 + lint 내부 심의
                   → 수정 확정 → state.json 저장 (step="reviewed")

04_approve.py   → 요약 출력 후 y/n 대기
05_execute.py   → pytest 실행 → state.json에 결과 저장

06_heal.py      → 실패 분석 → heal_context 저장 (LLM 없음)

06a_dialog.py   → 컨텍스트 수집·출력 (파일 병렬 읽기, LLM 없음)
[심의 Agent 1회] → DELIBERATION_CONTEXT 주입 → 트레이스백 진단·패치 내부 심의
                   → 패치 확정 → test_generated.py 직접 수정
                   → 05_execute.py 재실행 (최대 3회)
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
   **[심의 Agent 1회 호출]** — 아래 프롬프트 형식으로 single agent 실행:
   ```
   아래 컨텍스트를 바탕으로 사수(Senior QA Lead)와 부사수(Junior QA Engineer) 두 관점을
   내부적으로 시뮬레이션하여 테스트 plan을 확정하라.

   team_charter: {ctx.team_charter}
   senior_role: {ctx.senior_role}
   junior_role: {ctx.junior_role}
   dom_info: {ctx.dom_info}
   test_cases: {ctx.test_cases}

   출력 형식:
   1. state.json에 plan 저장, step = "planned"

   plan 각 항목:
   { case_name, case_type, description, steps:[{action,selector,value}], assertion:{type,expected} }
   - structured 케이스: precondition/steps/expected 직접 반영
   - natural 케이스: dom_info 기반 steps/assertion 자동 추론
   ```

**3.** `python scripts/02_generate.py` 실행
   완료 후 plan 기반으로 `tests/generated/test_generated.py` 직접 완성
   - 함수명은 반드시 영문 snake_case: test_{english_snake_case} (한글 제목이어도 영어로 번역)

**4.** `python scripts/03_lint.py` 실행

**5.** `python scripts/03a_dialog.py` 실행
   출력에서 DELIBERATION_CONTEXT JSON 추출.
   **[심의 Agent 1회 호출]** — 아래 프롬프트 형식으로 single agent 실행:
   ```
   아래 컨텍스트를 바탕으로 코드 리뷰를 수행하고 필요 시 코드를 직접 수정하라.

   team_charter: {ctx.team_charter}
   generated_code: {ctx.generated_code}
   lint_result: {ctx.lint_result}
   plan: {ctx.plan}

   수행할 작업:
   1. lint 이슈 수정 (있는 경우 tests/generated/test_generated.py 직접 편집)
   2. 셀렉터·assertion 검토 후 개선 사항 반영
   3. state.json에 review_summary 저장, step = "reviewed"
   4. 리뷰 중 발견된 문제점이 있으면 agents/lessons_learned.md 해당 섹션에 추가
      형식 (발견 사항 없으면 생략):
      ```
      ### [코드 리뷰] {날짜} — {테스트 파일}
      - **문제**: {발견된 문제 내용}
      - **수정**: {적용한 수정 내용}
      - **재발 방지**: {동일 실수를 피하기 위한 규칙}
      ```
   ```

**6.** `python scripts/04_approve.py` 실행 → 사용자에게 y/n 요청
   반려 시 rejection_reason 저장 → 3번으로 돌아가 코드 재작성

**7.** 승인 시 `python scripts/05_execute.py` 실행

**8.** `python scripts/06_heal.py` 실행
   - 종료코드 0: 전체 통과 → 완료
   - 종료코드 1: heal_context 저장됨 →
     `python scripts/06a_dialog.py` 실행
     출력에서 DELIBERATION_CONTEXT JSON 추출.
     **[심의 Agent 1회 호출]** — 아래 프롬프트 형식으로 single agent 실행:
     ```
     아래 컨텍스트를 바탕으로 실패를 진단하고 코드를 직접 패치하라.

     generated_code: {ctx.generated_code}
     heal_context: {ctx.heal_context}
     dom_info: {ctx.dom_info}

     수행할 작업:
     1. 각 failure의 traceback 분석 → 오류 유형 분류 (Locator/Assertion/Timeout/URL)
     2. tests/generated/test_generated.py 직접 패치

     패치 기준:
     - Locator 오류 → dom_info 셀렉터와 대조해 수정
     - Assertion 오류 → 실제 텍스트/상태로 기댓값 수정
     - Timeout → wait_for_selector 또는 expect timeout 조정
     - URL 오류 → BASE_URL 또는 goto 인자 수정
     ```
     → 7번으로 돌아가 재실행
   - 종료코드 2: 최대 힐링 횟수 초과 → 사용자에게 수동 수정 요청

대시보드 실행 (선택): `python agents/dashboard/serve.py`

---

## 병렬 파이프라인 (다중 URL)

여러 URL을 동시에 테스트할 때 사용한다. 각 URL은 독립된 worker 환경에서 실행된다.

### 오케스트레이터 실행 순서

```
python run_qa_parallel.py --targets config/targets.json
  → parallel/00_split.py 호출
     - URL별 workers/{worker_id}/ 디렉토리 생성
     - DOM 분석 (URL당 1회)
     - workers/{worker_id}/state.json 초기화 (step="analyzed", approval_status="approved")
  → parallel/batch_state.json 생성
  → Claude Code에 subagent 실행 지시 출력
```

Claude Code(오케스트레이터)는 batch_state.json을 읽고 Agent tool로 각 worker를 **동시에** 실행한다.

### Subagent 지시 형식

각 subagent는 아래 지시를 받아 독립적으로 실행한다. **모든 독립 작업은 병렬로 처리한다.**

```
worker_dir  = "workers/{worker_id}"   (batch_state.json에서 읽음)
group_dir   = batch_state.json의 workers[n].group_dir   (예: "login")
group_label = batch_state.json의 workers[n].group_label (예: "login_001")

다음을 순서대로 실행할 것. 스크립트는 cwd={worker_dir}로 실행한다.

1. [건너뜀] 01_analyze.py — dom_info가 이미 state.json에 있음

2. python ../../scripts/02a_dialog.py  (cwd={worker_dir})
   출력의 DELIBERATION_CONTEXT JSON을 추출해 심의 agent 1회 호출:
   - 사수/부사수 내부 시뮬레이션 → plan 확정
   - {worker_dir}/state.json에 plan 저장, step="planned"

3. python ../../scripts/02_generate.py  (cwd={worker_dir})

4. {worker_dir}/tests/generated/test_generated.py 를
   plan 기반으로 직접 완성 (코드 작성)
   - 함수명은 반드시 영문 snake_case: test_{english_snake_case} 형식으로 작성
     (케이스 제목이 한글이어도 영어로 번역해서 사용)
   - BASE_URL 은 반드시 모듈 상단(import 바로 아래)에 선언
   - conftest.py 는 절대 재정의하지 말 것 (page fixture 이미 있음)

5. python ../../scripts/03_lint.py  (cwd={worker_dir})

6. python ../../scripts/03a_dialog.py  (cwd={worker_dir})
   출력의 DELIBERATION_CONTEXT JSON을 추출해 심의 agent 1회 호출:
   - 코드 + lint 내부 심의 → 수정 확정 → 코드 직접 편집
   - state["step"] = "reviewed" 업데이트

7. 완성된 테스트 코드를 tests/generated/{group_dir}/{group_label}.py 로 복사
   (프로젝트 루트 기준 절대 경로 사용)
   - group_dir  = batch_state.json의 workers[n].group_dir  (예: "login")
   - group_label = batch_state.json의 workers[n].group_label (예: "login_001")
   - 출력 예시: tests/generated/login/login_001.py

8. 오케스트레이터에 완료 보고
```

**주의:** 병렬 모드에서 subagent는 코드 생성까지만 담당한다.
실행(pytest)은 99_merge.py가 tests/generated/ 를 대상으로 일괄 수행한다.

### 전체 완료 후

모든 subagent 완료 후 오케스트레이터가 실행:
```
python parallel/99_merge.py
  → tests/generated/ 에서 pytest 일괄 실행
  → 실패 있으면 parallel/heal_context.json 저장 → 힐링 루프 진입
  → 결과 집계
  → tests/reports/parallel_index_{ts}.html 생성
  → workers/ 비우기
```

**힐링 루프 (99_merge.py 실패 시):**
- 종료 후 `parallel/heal_context.json`이 생성되면 Claude Code가 힐링을 수행한다.
- 힐링 기준은 단일 파이프라인과 동일:
  - Locator 오류 → DOM 셀렉터 수정
  - Assertion 오류 → 실제 텍스트/상태로 기댓값 수정
  - Timeout → wait_for_selector 또는 timeout 조정
  - URL 오류 → BASE_URL 또는 goto 인자 수정
- 패치 후 `python parallel/99_merge.py` 재실행 (최대 3회, heal_count 자동 누적)
- 힐링 시 `agents/lessons_learned.md`에 오류 패턴 추가:
  ```
  ### [힐링] {날짜} — {파일명}
  - **문제**: {traceback 요약}
  - **수정**: {적용한 패치 내용}
  - **재발 방지**: {동일 실수 방지 규칙}
  ```
- 3회 초과 시 수동 수정 요청

---

## 팀 자유 토론 파이프라인

사용자가 `run_team.py`를 실행하면 아래 순서로 진행한다.
어떤 주제든 사수/부사수가 토론하고, 사용자가 결론을 최종 승인한다.

### 실행 순서

```
python run_team.py --topic "주제"
  → discuss_state.json 초기화
```

**1.** `python scripts/team_discuss.py` 실행
   출력에서 `DELIBERATION_CONTEXT_START ~ END` 사이의 JSON 추출.
   **[심의 Agent — 멀티라운드 티키타카 진행]**

   > **핵심 규칙: 발언 1개 작성 → 즉시 dialog.json 저장 → 다음 발언 작성 → 즉시 저장 → 반복**
   > 배치 저장 금지. 대시보드가 3초마다 폴링하므로 한 발언씩 저장해야 실시간으로 보인다.

   ```
   아래 주제로 사수/부사수가 최소 3회 왕복(6발언) 실제 대화를 나눈 후 결론을 도출하라.

   topic: {ctx.topic}
   rejection_reason: {ctx.rejection_reason}  (재토론이면 반드시 반영)
   team_charter: {ctx.team_charter}
   team_notes: {ctx.team_notes}  (기존 결정 — 중복 지양)
   lessons_learned: {ctx.lessons_learned}

   ── 진행 방식 ──────────────────────────────────────────────────
   라운드마다 아래 순서를 반복한다. **각 발언 후 즉시 dialog.json에 append 저장.**

   [라운드 1]
   사수 발언 → dialog.json 저장 (messages에 append)
   부사수 반응 → dialog.json 저장

   [라운드 2]
   사수 반론·보완 → dialog.json 저장
   부사수 동의·추가 의견 → dialog.json 저장

   [라운드 3]
   사수 쟁점 정리·방향 제시 → dialog.json 저장
   부사수 최종 의견·예시 보완 → dialog.json 저장

   (필요 시 라운드 추가 — 주제가 복잡하거나 이견이 있으면 4~5라운드까지)

   [결론]
   from: "deliberation" 메시지로 합의 사항 정리 → dialog.json 저장
   session.status = "discussed", session.completed_at = 현재시각

   ── 역할 지침 ──────────────────────────────────────────────────
   사수:
   - 첫 발언: 문제·위험 요소 분석, 방향 제시
   - 이후 발언: 부사수 의견에 반응하며 보완하거나 반론
   - 단답 금지 — 구체적 근거와 예외 케이스 포함

   부사수:
   - 사수 발언에 직접 반응 (동의·보완·질문 중 택1)
   - "실제 적용 시 어려운 점"과 구체적 예시 제시
   - 무조건 동의 금지 — 현실적 관점 유지

   ── 저장 형식 (발언마다 즉시) ──────────────────────────────────
   dialog.json의 마지막 session.messages에 아래 형식으로 append:
   {
     "from": "senior" | "junior" | "deliberation",
     "timestamp": "현재시각 ISO",
     "content": "발언 내용"
   }
   deliberation 메시지에는 "status": "discussed" 추가.

   ⚠️ 저장 방식 강제 규칙:
   - 반드시 Edit tool로 messages 배열 마지막에 항목 1개씩 append
   - Write tool로 전체 파일 덮어쓰기 금지 (배치 저장 금지)
   - 발언 작성 → Edit 저장 → 다음 발언 작성 → Edit 저장 순서 엄수
   ```

   결론 저장:
   discuss_state.json → `{ "step": "discussed", "conclusion": "결론 (마크다운)" }`

**2.** 심의 완료 후 사용자에게 알림:
   "토론이 완료됐어요. 대시보드에서 결론을 확인하고 승인/반려해주세요."
   (대시보드 http://localhost:8765 → 해당 토론 세션 하단에 승인/반려 버튼이 표시됩니다)
   - 승인 시: 서버가 `agents/team_notes.md` 저장 + `pending_impl.json` 생성
     → 스케줄러(2분 내)가 `pending_impl.json` 감지 → Claude가 항목 자동 구현
     → 구현 완료 후 `pending_impl.json` 삭제, `team_notes.md`·`discuss_state.json` 초기화
   - 반려 시: rejection_reason 저장, discuss_state.step = "rejected" → 재토론 요청

---

## Healer 패치 기준
06_heal.py 실행 후 Claude Code가 heal_context를 보고 코드를 수정할 때:
- **Locator 오류** (`strict mode violation`, `Element not found`) → dom_info 셀렉터와 대조해 수정
- **Assertion 오류** (`Expected ... to contain`) → 실제 페이지 텍스트를 기댓값으로 수정
- **Timeout** → `page.wait_for_selector()` 추가 또는 `expect(..., timeout=10000)` 조정
- **URL 오류** → BASE_URL 또는 goto 인자 수정

---

## state.json 구조
```json
{
  "url": "",
  "test_cases": [],
  "step": "init | analyzed | planned | generated | reviewed | approved | done | heal_needed | heal_failed",
  "dom_info": {},
  "plan": [],
  "generated_file_path": "tests/generated/test_generated.py",
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

## 디렉토리
```
scripts/          단계별 실행 스크립트 (LLM 없음, 순수 Python)
  02a_dialog.py   Plan 대화 세션 초기화
  03a_dialog.py   코드 리뷰 대화 세션 초기화
  06a_dialog.py   힐링 대화 세션 초기화
agents/           사수-부사수 에이전트 시스템
  team_charter.md 팀 헌장 (협업 규칙, 역할 정의)
  dialog.json     팀 토론 대화 로그 전용 (QA 파이프라인 심의 기록 안 함)
  lessons_learned.md  실수 패턴 누적 (힐링·코드리뷰 시 자동 추가)
  team_notes.md   승인된 팀 결정사항
  roles/
    senior.md     사수 페르소나 및 행동 지침
    junior.md     부사수 페르소나 및 행동 지침
  dashboard/
    index.html    팀 토론 모니터링·승인 대시보드 UI
    serve.py      대시보드 로컬 서버 (python agents/dashboard/serve.py)
parallel/         병렬 파이프라인 스크립트
  00_split.py     URL별 worker 환경 초기화
  99_merge.py     결과 병합 + 통합 리포트 + 힐링 루프
  batch_state.json  전체 배치 상태 추적
  heal_context.json 병렬 힐링 루프용 traceback 저장 (실패 시 생성)
workers/          병렬 실행 시 URL별 독립 환경 (런타임 생성)
tests/generated/  Claude Code가 작성한 테스트 코드
tests/reports/    HTML 리포트
tests/screenshots/ 실패 시 스크린샷
testcases/        케이스 파일 (*.md) — 그룹별 서브폴더로 관리
config/
  pages.json      페이지명 → URL 매핑 (중앙 URL 레지스트리)
state.json        단일 파이프라인 상태
run_qa.py         단일 파이프라인 진입점
run_qa_parallel.py 병렬 파이프라인 진입점
doc/              내부 문서 (PROJECT_OVERVIEW, SCRIPTS_GUIDE, TEST_CASE_GUIDE)
```
