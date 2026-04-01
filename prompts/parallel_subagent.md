# 병렬 Subagent 코드 생성 프롬프트 (run_qa_parallel.py 후 사용)

아래 컨텍스트를 바탕으로 Playwright 테스트 코드를 생성하라.

url: {ctx.url}
dom_info: {ctx.dom_info}
test_cases: {ctx.test_cases}
test_data: {ctx.test_data}
team_charter: {ctx.team_charter}
lessons_learned: {ctx.lessons_learned}
output_path: {ctx.output_path}

수행할 작업:
1. **lessons_learned를 먼저 읽고** 과거 실수 패턴 확인 (같은 실수 반복 금지)
2. test_cases와 dom_info를 분석해 테스트 plan 수립
   - structured 케이스: precondition/steps/expected 직접 반영
   - natural 케이스: dom_info 기반 steps/assertion 자동 추론
3. plan 기반으로 완전한 Playwright 테스트 코드 작성 (lessons_learned 패턴 반영)
4. output_path에 직접 저장

## MUST NOT (절대 금지 — 위반 시 런타임 에러)
- `to_have_url()`, `to_have_text()` 등 Playwright matcher에 **lambda/callable 전달 금지** → 반드시 `re.compile()` 사용
- 공유 헬퍼 파일(helpers.py 등) **생성/import 금지** → 각 파일이 자체 완결
- conftest.py **재정의 금지** (page fixture 이미 있음)
- test_data.json 경로에서 `.parent` **3번 사용 금지** → `tests/generated/{group}/`에서 프로젝트 루트까지 `.parent` 4번 필요
- 입력값 **하드코딩 금지** → 반드시 test_data.json에서 읽기
- `ENV:` 프리픽스 데이터는 **리터럴 사용 금지** → `os.environ.get()` 처리, 미설정 시 `pytest.skip()`

## MUST (필수 준수)
- import: `pytest`, `from playwright.sync_api import expect`, `json`, `re`, `from pathlib import Path`
- `BASE_URL = "{url}"` (모듈 상단 선언)
- `TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "test_data.json"`
- 함수명: `test_{english_snake_case}` (한글 제목도 영어로 번역)
- 파일당 테스트 함수 1개 (tc_*.md 1:1 매핑)
- `page.goto(BASE_URL)`로 시작
- `expect()`로 assertion, URL 패턴은 `re.compile()` 사용

## SHOULD (권장)
- Cafe24 로그인 폼: `#member_id` / `#member_passwd` ID 사용, 버튼은 `a.btnSubmit`
- 로그인 후 팝업/오버레이: JS evaluate로 `display:none` 강제 숨김
- alert 검증: 특정 메시지 대신 alert 발생 여부만 확인
- `to_have_text` 대신 `to_contain_text` 사용 (공백 대응)
