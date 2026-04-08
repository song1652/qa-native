# 파이썬 파일 실행 가이드

> **독자**: 사람 — 모든 .py 파일의 역할과 실행 방법 정리. 에이전트가 읽지 않음.

---

## 한눈에 보기

```
직접 실행하는 파일 (진입점)
├── run_qa.py                  ← QA 자동화 시작 (단일 URL)
├── run_qa_parallel.py         ← QA 자동화 시작 (여러 URL 동시)
├── run_team.py                ← 팀 토론 시작 (터미널용, 대시보드 권장)
├── agents/dashboard/serve.py  ← 모니터링 대시보드 서버
├── parallel/99_merge.py       ← 병렬 실행 완료 후 결과 통합
└── telegram_bot.py            ← 텔레그램 봇 서버

Claude가 자동으로 호출하는 파일 (직접 실행 불필요)
└── scripts/
    ├── 01_analyze.py          파이프라인 1단계: DOM 분석
    ├── 02a_dialog.py          파이프라인 2단계: Plan 심의 준비
    ├── 02_generate.py         파이프라인 3단계: 코드 뼈대 생성
    ├── 03_lint.py             파이프라인 4단계: lint 검사
    ├── 03a_dialog.py          파이프라인 5단계: 코드 리뷰 심의 준비
    ├── 04_approve.py          파이프라인 6단계: 사용자 승인 (터미널)
    ├── 05_execute.py          파이프라인 7단계: pytest 실행
    ├── 06_heal.py             파이프라인 8단계: 실패 분석
    ├── 06a_dialog.py          파이프라인 9단계: 힐링 심의 준비
    ├── team_discuss.py        팀 토론: 심의 컨텍스트 준비
    ├── team_approve.py        팀 토론: 결론 승인 (터미널용, 대시보드 권장)
    ├── check_pending_impl.py  훅: 승인 항목 자동 구현 트리거 감지
    └── parse_cases.py         라이브러리: 테스트케이스 파일 파서
```

---

## 직접 실행하는 파일

### `run_qa.py` — QA 자동화 시작 (단일 URL)

테스트할 URL과 케이스 폴더를 지정하면 Claude에게 파이프라인 실행 지시를 출력합니다.

```powershell
# 케이스 폴더 지정 (권장) — 폴더 내 tc_*.md 파일 전체를 자동 읽음
python run_qa.py --url https://example.com/login --cases testcases/login/

# 단일 파일 지정
python run_qa.py --url https://example.com/login --cases testcases/login/tc_01_login_success.md
```

**동작 순서:**
1. `testcases/` 폴더에서 케이스 파일 읽기
2. `state.json` 생성 (URL + 케이스 목록)
3. 케이스가 1개면 → 단일 파이프라인 지시 출력
4. 케이스가 2개 이상이면 → `run_qa_parallel.py`와 동일하게 병렬 파이프라인으로 자동 전환

---

### `run_qa_parallel.py` — QA 자동화 시작 (여러 URL 동시)

`config/pages.json`에 등록된 URL을 기반으로 여러 URL을 동시에 테스트합니다.

```powershell
# pages.json에 등록된 모든 URL 자동 스캔
python run_qa_parallel.py

# 특정 targets.json 지정
python run_qa_parallel.py --targets config/targets.json
```

**`config/pages.json` 형식:**
```json
{
  "login": "https://example.com/login",
  "mypage": "https://example.com/mypage"
}
```
키 이름 = `testcases/` 하위 폴더명과 일치해야 합니다.

**동작 순서:**
1. `config/pages.json` 읽기 → URL 목록 확인
2. `parallel/00_split.py` 호출 → URL별 `workers/` 환경 생성 + DOM 분석
3. Claude에게 각 worker를 동시 실행하라는 지시 출력
4. 모든 worker 완료 후: `python parallel/99_merge.py` 실행

---

### `parallel/99_merge.py` — 병렬 실행 결과 통합

모든 worker의 코드 생성이 완료된 후 실행합니다. Claude가 지시를 출력하면 그때 실행합니다.

```powershell
python parallel/99_merge.py
# 특정 그룹만 실행
python parallel/99_merge.py --group saintcore
```

**동작:**
1. `tests/generated/` 폴더 pytest 일괄 실행 (병렬 4 workers)
2. **실패 시**: `parallel/heal_context.json` 생성 → Claude Code가 traceback 분석 후 패치 → 재실행 (최대 3회)
3. 전체 통과 시: `tests/reports/parallel_index_{날짜시간}.html` 리포트 생성
4. `workers/` 폴더 정리

> 리포트는 같은 `group_dir`(폴더명)의 케이스를 하나의 그룹 카드로 묶어 표시합니다.

---

### `agents/dashboard/serve.py` — 모니터링 대시보드

사수/부사수 대화를 실시간으로 보고, 팀 토론을 진행·승인할 수 있는 웹 UI 서버입니다.

```powershell
python agents/dashboard/serve.py
# 브라우저에서 http://localhost:8765 자동 열림
```

**대시보드에서 할 수 있는 것:**
| 기능 | 방법 |
|---|---|
| 팀 토론 실시간 모니터링 | 사수/부사수 티키타카 대화가 발언마다 실시간 표시 (SSE) |
| 팀 토론 시작 | 팀 토론 섹션 주제 입력 → 토론 시작 버튼 |
| 토론 결론 항목별 승인 | 각 항목 ✓/✗ 버튼 클릭 |
| 승인 후 자동 구현 | 전체 투표 완료 시 스케줄러(2분 내)가 자동으로 Claude에게 구현 지시 |
| 대화 초기화 | 우측 상단 "대화 초기화" 버튼 |

> **참고**: QA 파이프라인 심의(Plan·코드리뷰·힐링)는 대시보드에 표시되지 않습니다.
> 결과는 `state.json`에 저장되며, 터미널 로그에서 확인할 수 있습니다.

**서버 재시작 방법 (코드 변경 후):**
```powershell
# 포트 확인
netstat -ano | findstr :8765
# PID 종료
taskkill /PID [숫자] /F
# 재시작
python agents/dashboard/serve.py
```

---

### `run_team.py` — 팀 토론 시작 (터미널용)

> **권장:** 대시보드의 "토론 시작" 버튼 사용. `run_team.py`는 대시보드 없이 터미널에서만 쓸 때 사용.

```powershell
python run_team.py --topic "함수명 영문 번역 기준 정의"
python run_team.py  # 주제를 대화형으로 입력
```

**동작:** `discuss_state.json` 생성 후 다음 단계 안내 출력.
이후 Claude에게 직접 "팀 토론 진행해줘"라고 요청하면 됩니다.

---

### `telegram_bot.py` — 텔레그램 봇 서버

텔레그램에서 Claude에게 QA 명령을 보낼 수 있는 봇 서버입니다.

```powershell
python telegram_bot.py
```

**사용 방법:** 텔레그램 앱에서 봇에게 메시지를 보내면 Claude가 응답합니다.
Claude Code가 실행 중인 상태에서 함께 구동해야 합니다.

---

## Claude가 자동으로 호출하는 파일 (scripts/)

> 아래 파일들은 **직접 실행하지 않습니다.** `run_qa.py` 실행 후 Claude가 순서대로 자동 호출합니다.
> 문제 해결 목적으로 개별 실행이 필요할 때만 참고하세요.

### 단일 파이프라인 순서

```
01_analyze.py
  → URL에 접속해 DOM 구조 추출 (input, button, form, link 등)
  → state.json에 dom_info 저장

02a_dialog.py
  → Plan 심의에 필요한 파일들을 병렬로 읽어 JSON으로 출력
  → Claude가 이 출력을 보고 사수/부사수 심의 진행

02_generate.py
  → plan 기반으로 tests/generated/test_generated.py 뼈대 생성
  → Claude가 뼈대를 완성 코드로 채움

03_lint.py
  → flake8으로 생성된 테스트 코드 품질 검사
  → state.json에 lint_result 저장

03a_dialog.py
  → 코드 리뷰 심의에 필요한 파일들을 병렬로 읽어 JSON으로 출력
  → Claude가 lint 결과 + 코드를 보고 리뷰 진행

04_approve.py
  → 리뷰 요약을 출력하고 사용자에게 y/n 입력 대기
  → n이면 rejection_reason 저장 후 코드 재작성으로 돌아감

05_execute.py
  → pytest로 테스트 실행
  → state.json에 execution_result 저장

06_heal.py
  → 실패한 테스트의 traceback을 수집해 heal_context 저장
  → 종료코드 0=전체 통과, 1=실패 있음, 2=힐링 횟수 초과

06a_dialog.py
  → 힐링 심의에 필요한 파일들을 병렬로 읽어 JSON으로 출력
  → Claude가 traceback을 분석해 코드 패치 후 05_execute.py 재실행
```

**개별 실행이 필요한 경우 (cwd = 프로젝트 루트):**
```powershell
python scripts/01_analyze.py
python scripts/03_lint.py
python scripts/05_execute.py
# 등...
```

---

### 팀 토론 관련

| 파일 | 역할 | 실행 주체 |
|---|---|---|
| `scripts/team_discuss.py` | 토론 컨텍스트 준비 + dialog.json 세션 생성 | 대시보드 버튼 클릭 시 자동 실행 |
| `scripts/team_approve.py` | 결론 표시 후 y/n 승인 (터미널용) | 대시보드 승인 버튼으로 대체됨 |

---

### 라이브러리 파일

| 파일 | 역할 | 직접 실행 |
|---|---|---|
| `scripts/parse_cases.py` | `.md`/`.json` 테스트케이스 파일 파서 | ❌ (run_qa.py가 import해서 사용) |
| `tests/conftest.py` | pytest browser/page fixture 정의 | ❌ (pytest가 자동 로드) |

---

## 설정 파일 (config/)

| 파일 | 역할 | 예시 키 |
|---|---|---|
| `config/pages.json` | 페이지명 → URL 매핑. `run_qa_parallel.py`가 자동 참조 | `"login": "https://..."` |
| `config/test_data.json` | 테스트 입력값 중앙 관리. 테스트 코드에서 하드코딩 금지, 이 파일에서 읽어 사용 | `"login": { "valid_user": {...} }` |

`test_data.json` 형식:
```json
{
  "login": {
    "valid_user": { "username": "tomsmith", "password": "SuperSecretPassword!" },
    "invalid_user": { "username": "wrong", "password": "wrong" }
  },
  "mypage": {
    "edit_user": { "name": "홍길동", "email": "test@example.com" }
  }
}
```
키는 `pages.json`의 페이지명과 일치시킵니다.

---

## 상태 파일 (실행 결과가 저장되는 곳)

| 파일 | 저장 내용 | 생성 시점 |
|---|---|---|
| `state.json` | 단일 파이프라인 전체 상태 (dom_info, plan, review_summary, heal_context 등) | `run_qa.py` 실행 시 |
| `discuss_state.json` | 팀 토론 상태 (주제, 결론, 투표 항목) | 대시보드 토론 시작 시 |
| `agents/dialog.json` | **팀 자유 토론 대화 로그 전용** (QA 파이프라인 심의는 기록 안 함) | 팀 토론 시작 시 |
| `agents/team_notes.md` | 승인된 팀 결정사항 (구현 완료 후 초기화) | 토론 항목 전체 투표 완료 시 |
| `agents/lessons_learned.md` | 테스트 실패·코드리뷰 실수 패턴 누적 | 힐링·코드리뷰 심의 완료 시 |
| `pending_impl.json` | 승인 후 구현 대기 항목 (스케줄러가 감지해 자동 구현) | 대시보드 전체 투표 완료 시 |
| `parallel/batch_state.json` | 병렬 파이프라인 워커 목록·상태 | `run_qa_parallel.py` 실행 시 |
| `parallel/heal_context.json` | 병렬 파이프라인 실패 traceback (힐링 루프용) | `99_merge.py` 실패 시 |
