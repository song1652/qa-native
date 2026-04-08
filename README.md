# QA Automation — Claude Code Native

> **독자**: 사람 — 신규 진입점. 설치·실행 방법과 내부 문서 링크 모음.

API 비용 없이 Claude Code 토큰만으로 동작하는 QA 자동화 시스템.

---

## 실행 파일 목록

| 파일 | 언제 실행? | 하는 일 |
|---|---|---|
| `run_qa.py` | 단일 URL 테스트 시작 | state.json 생성 후 Claude에게 파이프라인 실행 지시 |
| `run_qa_parallel.py` | 여러 URL 동시 테스트 | pages.json 기반 워커 생성 + 병렬 실행 지시 |
| `run_team.py` | 팀 토론 주제 등록 | discuss_state.json 생성 (대시보드 버튼으로 대체 가능) |
| `agents/dashboard/serve.py` | 모니터링 대시보드 실행 | http://localhost:8765 에서 대화·승인·토론 관리 |
| `parallel/99_merge.py` | 병렬 실행 완료 후 | pytest 일괄 실행 + HTML 리포트 생성 + workers 정리 |

> **scripts/ 폴더 안의 파일들은 직접 실행하지 않습니다.** Claude가 파이프라인 순서에 따라 자동으로 호출합니다.

---

## 설치

```bash
pip install -r requirements.txt
playwright install chromium
```

---

## 실행

```bash
python run_qa.py --url https://example.com/login --cases testcases/login/cases.md
```

케이스 수에 따라 자동 분기됩니다:

| 케이스 수 | 동작 |
|---|---|
| 1개 | 단일 파이프라인 — `state.json` 생성 후 Claude Code가 순차 실행 |
| N개 | 병렬 파이프라인 — 케이스별 worker 자동 생성, Claude Code가 동시 실행 |

---

## 테스트 케이스 작성

케이스는 `testcases/` 하위 그룹 폴더에 `.md` 파일로 작성합니다. **1파일 = 1케이스.**

```
testcases/
  login/
    tc_01_login_success.md
    tc_02_wrong_password.md
  mypage/
    tc_01_profile_edit.md
```

**케이스 파일 형식:**

```markdown
# 정상 로그인 성공

## Precondition
0. 로그인 페이지 접속 상태

## Steps
1. username 필드에 tomsmith 입력
2. password 필드에 SuperSecretPassword! 입력
3. Login 버튼 클릭

## Expected
- You logged into a secure area! 메시지가 표시되어야 한다.
```

자세한 작성 규칙: `doc/TEST_CASE_GUIDE.md`

---

## 병렬 파이프라인 직접 실행 (선택)

`run_qa.py`의 자동 라우팅 대신 targets.json으로 직접 제어할 때:

```bash
python run_qa_parallel.py --targets testcases/targets_login.json
# Claude Code가 각 worker를 동시에 실행 (코드 생성)
python parallel/99_merge.py
# pytest 일괄 실행 + HTML 리포트 + workers 정리
```

### targets.json 작성법

**폴더 지정 (권장)** — 폴더 내 `*.md` 파일 각각을 worker로 자동 확장:

```json
[
  {"url": "https://example.com/login", "cases": "testcases/login"}
]
```

**파일 직접 지정** — 특정 케이스만 선택:

```json
[
  {"url": "https://example.com/login", "cases": "testcases/login/tc_01_login_success.md"},
  {"url": "https://example.com/login", "cases": "testcases/login/tc_02_wrong_password.md"}
]
```

**여러 그룹 혼합:**

```json
[
  {"url": "https://example.com/login",  "cases": "testcases/login"},
  {"url": "https://example.com/mypage", "cases": "testcases/mypage"}
]
```

- 같은 URL은 DOM 분석 캐시 사용 (재분석 생략)
- `cases` 경로는 프로젝트 루트 기준 상대 경로

---

## 산출물

| 파일 | 내용 |
|---|---|
| `tests/generated/{group}/{label}.py` | Claude Code가 작성한 테스트 코드 |
| `tests/reports/parallel_index_{ts}.html` | 통합 HTML 리포트 |
| `tests/screenshots/*.png` | 실패 케이스 자동 스크린샷 |

---

## 파일 구조

| 파일/폴더 | 역할 |
|---|---|
| `run_qa.py` | 파이프라인 진입점 (단일/병렬 자동 분기) |
| `run_qa_parallel.py` | 병렬 파이프라인 직접 실행용 |
| `scripts/01~06_*.py` | 단계별 스크립트 (LLM 없음) |
| `scripts/02a,03a,06a_dialog.py` | 심의 컨텍스트 수집·출력 |
| `parallel/00_split.py` | worker 환경 초기화 + DOM 분석 |
| `parallel/99_merge.py` | pytest 일괄 실행 + 리포트 + workers 정리 |
| `agents/` | 사수-부사수 역할 정의, 팀 토론 dialog 로그, lessons_learned |
| `testcases/` | 테스트 케이스 `.md` 파일 |
| `config/pages.json` | 페이지명 → URL 매핑 |
| `config/test_data.json` | 테스트 입력값 중앙 관리 (계정, 폼 데이터 등) |
| `CLAUDE.md` | Claude Code 행동 지침 |

---

## 트러블슈팅

| 증상 | 원인 | 해결 |
|---|---|---|
| `batch_state.json 없음` | worker 초기화 미실행 | `run_qa.py` 또는 `run_qa_parallel.py` 재실행 |
| `tests/generated/` 파일 없음 | subagent 코드 생성 미완료 | Claude Code에 subagent 재실행 요청 |
| 특정 케이스 FAIL | assertion / locator 오류 | 해당 `.py` 파일 직접 확인 후 수정, 또는 Healer 재실행 |
| 스크린샷 미생성 | conftest.py 중복 로드 | `tests/generated/` 하위에 conftest.py 없어야 함 |
| DOM 분석 실패 | 네트워크 / URL 오류 | URL 접근 가능 여부 확인 |

---

## 대시보드 (선택)

```bash
python agents/dashboard/serve.py
# http://localhost:8765 에서 팀 토론 실시간 모니터링·승인
```

대시보드는 **팀 자유 토론 전용**입니다. QA 파이프라인 심의 로그는 터미널과 `state.json`에서 확인하세요.

---

## 내부 문서 (`doc/`)

> `doc/` 폴더는 **사람 전용** 상세 문서 공간입니다. 에이전트(Claude)가 읽지 않습니다.

| 파일 | 내용 |
|---|---|
| [`doc/SCRIPTS_GUIDE.md`](doc/SCRIPTS_GUIDE.md) | **모든 .py 파일 역할·실행 방법 정리** |
| [`doc/PROJECT_OVERVIEW.md`](doc/PROJECT_OVERVIEW.md) | 아키텍처·설계 의도 상세 |
| [`doc/TEST_CASE_GUIDE.md`](doc/TEST_CASE_GUIDE.md) | 테스트케이스 작성 규칙 |
