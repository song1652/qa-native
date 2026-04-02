# QA-Native — 아키텍처 문서

> **독자**: 사람 — 내부 설계·아키텍처 문서. 에이전트가 읽지 않음.
> **Claude Code가 LLM 역할을 직접 수행하는 API-Free QA 자동화 파이프라인**

---

## 핵심 설계 원칙

| 원칙 | 내용 |
|---|---|
| **API-Free** | `anthropic`, `openai`, `langchain` 등 외부 LLM SDK 일절 미사용 |
| **Claude Code = 두뇌** | 전략 수립, 코드 작성, 리뷰, 실패 패치를 직접 수행 |
| **스크립트 = 실행 도구** | 01~06 스크립트는 DOM 추출·lint·pytest·결과 수집만 담당 |
| **state/pipeline.json 중심** | 모든 단계 결과가 하나의 파일에 누적 → 단계 간 컨텍스트 공유 |
| **단일 심의 Agent** | 사수/부사수 두 관점을 한 번의 Agent 호출로 내부 시뮬레이션 |
| **컨텍스트 주입** | `02a/03a/06a_dialog.py`가 파일을 병렬 읽기 후 JSON으로 출력 → Agent가 추가 파일 읽기 불필요 |

---

## 아키텍처

### 단일 파이프라인

```
┌────────────────────────────────────────────────┐
│               Claude Code (두뇌)               │
│  DOM 분석 해석 → 테스트 전략 수립              │
│  테스트 코드 직접 작성                          │
│  실패 트레이스백 분석 → 코드 자동 패치          │
└──────────────────┬─────────────────────────────┘
                   │  읽기 / 쓰기
                   ▼
         state/pipeline.json
                   │
       ┌───────────┼───────────┐
       ▼           ▼           ▼
  Python        Playwright   pytest
  스크립트      (브라우저)   (테스트 실행)
 01~06_*.py    Chromium      HTML 리포트
```

### 병렬 파이프라인

```
testcases/{group}/tc_*.md  (1파일 = 1케이스)
      ↓                     예: myshop/ (N개)
run_qa_parallel.py
      ↓
config/pages.json → URL 조회 + testcases/ 폴더 자동 스캔
      ↓
DOM 분석 (URL당 1회, 캐시)
      ↓
PARALLEL_SUBAGENT_CONTEXTS 출력
      ↓
오케스트레이터 Claude (Agent tool)
  ┌──────────┬──────────┬──────────┐
  │Subagent 1│Subagent 2│Subagent N│  ← 동시 실행
  │ tc_01    │ tc_02    │ tc_N     │
  │plan→코드 │plan→코드 │plan→코드 │
  └──────────┴──────────┴──────────┘
      ↓
  tests/generated/{group}/{label}.py  저장
      ↓
parallel/99_merge.py
  pytest tests/generated/ 일괄 실행
  통합 HTML 리포트 생성
  실패 시 state/heal_context.json → 힐링 루프 (최대 3회)
```

### 심의 Agent 흐름 (Plan / Code Review / Healing)

```
*a_dialog.py 실행
  └─ team_charter.md, senior.md, junior.md, lessons_learned.md, 코드 병렬 읽기
  └─ DELIBERATION_CONTEXT_START ... END  JSON 출력

오케스트레이터 Claude가 JSON 추출
  └─ 심의 Agent 1회 호출 (사수/부사수 내부 시뮬레이션)
       └─ plan / review / patch 확정
       └─ state/pipeline.json 업데이트 (결과 저장)
       └─ 필요 시 agents/lessons_learned.md 오류 패턴 추가

※ dialog.json은 팀 자유 토론 전용. QA 파이프라인 심의는 state/pipeline.json에만 기록됨.
```

### 팀 토론 흐름

```
대시보드 "토론 시작" 또는 run_team.py
  └─ team_discuss.py: 컨텍스트 수집 → DELIBERATION_CONTEXT 출력

Claude가 멀티라운드 티키타카 진행 (최소 3라운드)
  └─ 발언마다 agents/dialog.json에 즉시 append (Edit tool, 배치 금지)
  └─ 대시보드 SSE로 실시간 표시

결론 도출 → 사용자가 대시보드에서 항목별 승인/반려
  └─ 승인 시: team_notes.md 저장 + pending_impl.json 생성
  └─ 훅(check_pending_impl.py) → Claude가 자동 구현
```

---

## Healer (자가 치유)

테스트 실패 시 `06_heal.py`가 traceback을 수집하고 Claude Code가 패치합니다. 최대 3회 자동 시도.
스크린샷은 최종 실패 시에만 저장됩니다 (힐링 중간 실행에서는 매번 초기화).
실패 스크린샷이 heal_context에 자동 연결되며, traceback만으로 원인 불명확 시 Playwright MCP 도구로 실제 페이지의 현재 DOM/텍스트를 확인할 수 있습니다.

> 패치 기준표·힐링 완료 체크리스트·MCP 시각 검증 절차는 [`CLAUDE.md`](../CLAUDE.md) "공통: 힐링 패치 기준" 참조.

---

## 기술 스택

Python 3.13 / Playwright (Chromium) / pytest / flake8 / Claude Code (API 없음)

> 대시보드: Python ThreadingHTTPServer + SSE + Vanilla JS (포트 8765)
> 상세 API·기능: [`SCRIPTS_GUIDE.md`](SCRIPTS_GUIDE.md) 참조
