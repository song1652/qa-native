# 디렉토리 구조

```
scripts/            단계별 실행 스크립트 (LLM 없음, 순수 Python)
  01_analyze.py     DOM 추출
  02_generate.py    코드 뼈대 생성
  02a_dialog.py     Plan 대화 세션 초기화
  03_lint.py        flake8 검사
  03a_dialog.py     코드 리뷰 대화 세션 초기화
  04_approve.py     (사용 중단 — 승인 단계 제거됨)
  05_execute.py     pytest 실행
  06_heal.py        실패 분석
  06a_dialog.py     힐링 대화 세션 초기화
  team_discuss.py   팀 토론 초기화
  parse_cases.py    tc_*.md 파싱
  _python.py        .venv 경로 자동 감지
  _paths.py         중앙 경로 상수 (state/, logs/)
  _constants.py     파이프라인 종료 코드 상수
  heal_utils.py     힐링 공용 유틸리티 (classify_error, extract_key_lines 등)
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
  heal_stats.json   힐링 오류 패턴별 빈도 카운터 (06_heal.py가 자동 업데이트)

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
tests/test_core_parsers.py  핵심 파서 유닛 테스트

testcases/          케이스 파일 (tc_*.md) — 그룹별 서브폴더로 관리
  heroku/           heroku 테스트케이스 (20개)
config/
  pages.json        페이지명 → URL 매핑 (login, secure, heroku)
  test_data.json    테스트 입력값 (heroku: valid_user, invalid_user, js_prompt, forgot_email)

.claude/skills/     스킬 프레임워크 (공식 SKILL.md 표준)
  playwright-best-practices/
    SKILL.md        Python Playwright 정적 베스트프랙티스
  heal-patterns/
    SKILL.md        힐링 오류 유형별 패치 전략 가이드라인

knowledge/          QA 지식 베이스
  qa-checklist.md   스모크 항목 + Playwright 작성 체크리스트
  team-rules.md     팀 내규 (TC ID, 우선순위, 소통, 리뷰, 이슈 관리)

templates/          문서 템플릿
  tc-template.md    테스트케이스 작성 템플릿
  report-template.md 테스트 리포트 템플릿
  issue-template.md  이슈(버그) 리포트 템플릿

reports/issues/     이슈 추적 파일 (ISSUE-{날짜}-{번호}.md)
 
```
