# 디렉토리 구조

```
_bootstrap.py       프로젝트 진입점 공통 경로 설정 (루트 스크립트가 import)

scripts/            단계별 실행 스크립트 (LLM 없음, 순수 Python, 패키지 구조)
  01_analyze.py     DOM 추출 (단일 브라우저, 서브페이지 Semaphore(8) 병렬, 9가지 다중 셀렉터 전략, 동적 UI/우클릭 메뉴 캡처, 정적 TTL 7일·동적 TTL 24h)
  02_generate.py    코드 뼈대 생성
  02a_dialog.py     Plan 대화 세션 초기화
  03_lint.py        flake8 검사 → step=reviewed 설정
  03a_dialog.py     코드 리뷰 대화 세션 초기화
  04_approve.py     lint 리뷰 승인/반려 (종료코드 0=승인, 2=반려, 3=대시보드 승인 대기)
  05_execute.py     pytest 실행 (--only-failed, --no-report 플래그, 최대 8 workers)
  06_heal.py        실패 분석 (최대 3회 자동 패치, OMC ultraqa)
  06_auto_heal.py   자동 힐링 패치 (8개 정적 패턴: strict mode, timeout, to_have_class regex, triple_click, evaluate return, unicode encoding, modal timeout, 광고 제거 + heal_stats 빈출 패턴 보고)
  06a_dialog.py     힐링 대화 세션 초기화
  team_discuss.py   팀 토론 초기화
  dom_helpers.js    JS 공통 유틸 (isVisible·esc·getSelectorsSimple) — _js()가 JS 스크립트에 자동 주입
  parse_cases.py    tc_*.md 파싱
  _generate_plan.py 테스트 케이스별 실행 계획 생성
  _python.py        .venv 경로 자동 감지 (PROJECT_ROOT를 _paths.py에서 import)
  _paths.py         중앙 경로 상수 (state/, logs/) + read_state/write_state 원자적 I/O (FSM 전이 자동 검증 내장)
  _constants.py     파이프라인 종료 코드 상수 + VALID_TRANSITIONS 맵 + assert_valid_transition()
  __init__.py       scripts 패키지 초기화 (외부 import 가능)
  heal_utils.py     힐링 공용 유틸리티 (classify_error 7분류, extract_key_lines, append_lessons→_auto.md 등)
  result_parser.py  pytest JSON 리포트 파싱 공통 모듈 (05_execute.py, 99_merge.py 공유)
  structured_log.py 구조화된 로그 (JSON Lines → logs/structured.jsonl)
  hook_utils.py     훅 스크립트 공통 유틸리티 (check_state() 함수)
  report_html.py    HTML 리포트 생성 (build_report, case_row — 단일/병렬 공통)
  team_approve.py   팀 토론 승인 (터미널용)
  sync_test_data.py test_data.json 동기화
  coverage_matrix.py  커버리지 매트릭스 생성 (tc_*.md 파싱 → state/coverage.json)
  flaky_detector.py   Flaky Test 감지기 (run_history.json 분석 → state/flaky_tests.json)
  _add_login_retry.py 병렬 세션 충돌 대응 — 생성된 테스트 파일에 로그인 재시도 로직 일괄 추가
  _complete_scaffolds.py scaffold 파일 완성 보조
  _fix_final_lint.py  lint 최종 패치 (특수 케이스)
  _fix_login_wait.py  로그인 대기 패치 (특수 케이스)
  _fix_string_split.py 문자열 분리 패치 (특수 케이스)
  _revert_login.py    로그인 패치 롤백
  check_pending_*.py  훅 스크립트 (hook_utils.check_state() 공통 사용)

agents/             사수-부사수 에이전트 시스템
  team_charter.md   팀 헌장 (협업 규칙, 역할 정의)
  IDENTITY.md       사수/부사수 페르소나 (말투, 성격, 대화 예시)
  SOUL.md           팀 원칙과 가치관
  dialog.json       팀 토론 대화 로그 전용 (QA 파이프라인 심의 기록 안 함)
  lessons_learned.md  큐레이션된 실수 패턴 (수동 관리, 힐링·코드리뷰 시 참조)
  lessons_learned_auto.md  자동 기록 힐링 로그 (heal_utils.py가 자동 추가)
  team_notes.md     승인된 팀 결정사항
  roles/
    senior.md       사수 행동 지침 (상세)
    junior.md       부사수 행동 지침 (상세)
  dashboard/
    index.html      파이프라인 모니터링·대시보드 UI
    serve.py        대시보드 로컬 서버 (python agents/dashboard/serve.py, 포트 8766)
    static/         정적 자산
      js/           JavaScript 뷰 컴포넌트
      css/          스타일시트

prompts/            심의 Agent 프롬프트 템플릿 (CLAUDE.md에서 분리)
  plan_deliberation.md      02a 심의 — plan 수립
  review_deliberation.md    03a 심의 — 코드 리뷰
  heal_deliberation.md      06a 심의 — 힐링 패치
  parallel_subagent.md      병렬 subagent 코드 생성
  team_discussion.md        팀 토론 멀티라운드
  examples/                 few-shot 예시 (JSON)
    plan_good.json          good plan 예시
    plan_bad.json           bad plan 예시 (흔한 실수)
    heal_patch.json         오류 유형별 before/after 패치 예시

state/              상태 파일 (런타임 생성)
  pipeline.json     단일 파이프라인 상태
  weverse_auth.json 위버스 세션 쿠키 저장 (tc_02 로그인 성공 시 자동 생성, 재사용으로 OTP 생략)
  discuss.json      팀 토론 상태
  parallel.json     병렬 파이프라인 상태
  quick.json        빠른 실행 상태
  heal_context.json 병렬 힐링 컨텍스트 (에러 분류, failure_groups, skipped_repeated, lessons_snapshot 포함)
  heal_stats.json   힐링 오류 패턴별 빈도 카운터 (06_heal.py가 자동 업데이트)
  run_history.json  실행 이력 (매 실행 시 자동 append — 메타 평가용)

logs/               실행 로그 (런타임 생성)
  run_qa.txt        단일 파이프라인 로그
  run_parallel.txt  병렬 파이프라인 로그
  merge.txt         99_merge.py 로그
  quick_run.txt     빠른 실행 로그
  structured.jsonl  구조화된 로그 (JSON Lines — step_start/end, test_fail, heal_skip 등)

parallel/           병렬 파이프라인 스크립트
  00_split.py       URL별 worker 환경 초기화 (workers/{id}/ 디렉토리 생성 + DOM 분석)
  99_merge.py       pytest 실행 + 통합 리포트 + 힐링 루프

tests/              테스트 산출물 + 리포트 + 스크린샷
  generated/        Claude Code가 작성한 테스트 코드 (그룹별 서브폴더, 각 __init__.py 필수)
    __init__.py     최상위 init
    demoqa/         demoqa 그룹
      __init__.py
      tc_*.py       개별 테스트 파일
    directcloud/    directcloud 그룹
      __init__.py
      tc_*.py       개별 테스트 파일
    heroku/         heroku 그룹
      __init__.py
      tc_*.py       개별 테스트 파일
    weverse/        weverse 그룹
      __init__.py
      tc_01_register_and_extract_wid.py   회원가입 후 WID 추출
      tc_02_login_and_extract_wid.py      기존 계정 로그인 + WID 추출 (세션 캐시)
      tc_03_google_login_and_extract_wid.py  Google OAuth 로그인 + WID 추출
      tc_04_community_post_crud.py        커뮤니티 팬 포스트 생성·수정·삭제
  reports/          HTML 리포트 (pytest 실행 결과)
  screenshots/      실패 시 스크린샷 (conftest.py 기반 자동 캡처)
  test_core_parsers.py  핵심 파서 유닛 테스트

testcases/          케이스 파일 (tc_*.md) — 그룹별 서브폴더로 관리
  demoqa/           demoqa 테스트 그룹 (120개 케이스)
    tc_*.md         개별 케이스 파일
  heroku/           heroku 테스트 그룹 (120개 케이스)
    tc_*.md         개별 케이스 파일
config/
  pages.json        페이지명 → URL 매핑 (키 = testcases/ 하위 폴더명)
  test_data.json    테스트 입력값 (키 = pages.json 페이지명)
  weverse.json      위버스 전용 설정 (existing_email/password, gmail_imap, community 등)

.claude/skills/     스킬 프레임워크 (공식 SKILL.md 표준)
  playwright-best-practices/
    SKILL.md        Python Playwright 정적 베스트프랙티스 (qa-native)
  heal-patterns/
    SKILL.md        힐링 오류 유형별 패치 전략 가이드라인 (qa-native)
  verify/
    SKILL.md        패치 후 05_execute 기반 3단계 증거 검증 (qa-native)
  skillify/
    SKILL.md        반복 패턴 → heal-patterns/lessons_learned 공식 등록 (qa-native)
  e2e-testing/
    SKILL.md        Playwright E2E 패턴, POM, flaky test 전략 (ECC)
  browser-qa/
    SKILL.md        배포 후 시각 검증, 4단계 QA 플로우 (ECC)
  verification-loop/
    SKILL.md        패치 완료 후 6단계 검증 체크리스트 (ECC)
  continuous-learning-v2/
    SKILL.md        신뢰도 기반 패턴 학습, lessons_learned 강화 (ECC)
  python-testing/
    SKILL.md        pytest 픽스처·파라미터화·mocking 전략 (ECC)

doc/                문서 (사람용, 에이전트 미참조)
  DIRECTORY.md      디렉토리 구조 (이 파일)
  PIPELINE_STATE.md state/pipeline.json 스키마 + discuss/parallel/quick.json 스키마
  PROJECT_OVERVIEW.md 아키텍처 설계 문서
  SCRIPTS_GUIDE.md  스크립트 CLI 옵션·실행 방법 (포트 8766)
  HEALING_GUIDE.md  힐링 완료 체크리스트 + MCP 시각 검증 절차
  TEAM_DISCUSSION.md 팀 토론 파이프라인 상세
  API_REFERENCE.md  CLI 옵션 완전 목록 + 대시보드 API 엔드포인트 (신규)
  PROMPTS_REFERENCE.md prompts/ 템플릿 입출력 스키마 (신규)

knowledge/          QA 지식 베이스
  qa-checklist.md   스모크 항목 + Playwright 작성 체크리스트
  team-rules.md     팀 내규 (TC ID, 우선순위, 소통, 리뷰, 이슈 관리)

templates/          문서 템플릿
  tc-template.md    테스트케이스 작성 템플릿
  report-template.md 테스트 리포트 템플릿
  issue-template.md  이슈(버그) 리포트 템플릿

reports/issues/     이슈 추적 파일 (ISSUE-{날짜}-{번호}.md)
 
```
