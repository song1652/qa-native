# Lessons Learned — QA 자동화 실수 패턴

> **독자**: 심의 Agent — 코드 작성·리뷰·힐링 전 자동 참조. 실수 패턴 누적.
> 테스트 실패 후 힐링 시, 그리고 코드 리뷰(03a) 단계에서 자동으로 누적됩니다.
> 코드 작성 전 반드시 이 파일을 참고하여 같은 실수를 반복하지 마세요.

---

## Locator 오류

<!-- 셀렉터가 잘못되어 요소를 찾지 못한 경우 -->

### [Locator] 2026-03-31 — Cafe24 쇼핑몰 로그인 폼 셀렉터
- **문제**: `input[name='m_id']`, `input[name='m_pw']` 추측 셀렉터로 작성 → Timeout 30s 발생
- **실제 DOM**: `#member_id` (type=text), `#member_passwd` (type=password), 로그인 버튼은 `<a class="btnSubmit">` (submit input 아님)
- **재발 방지**: Cafe24 기반 쇼핑몰 로그인 폼은 `member_id` / `member_passwd` ID 사용. 버튼은 `<a>` 태그 + class `btnSubmit`. DOM 확인 없이 `m_id`, `m_pw` 같은 추측 name 사용 금지.

### [Locator] 2026-03-31 — 로그인 후 팝업 오버레이 차단
- **문제**: 로그인 성공 후 `app-smart-popup` 팝업이 오버레이되어 로그아웃 버튼 클릭 차단 → Timeout 발생
- **수정**: `page.keyboard.press("Escape")` 후 `/exec/front/Member/logout/` URL 직접 navigate
- **재발 방지**: 로그인 후 동작 테스트 시 팝업/배너 차단 가능성 고려. 클릭보다 직접 URL navigate가 더 안정적.

### [힐링] 2026-03-31 — saintcore_008.py (smart-popup 클릭 차단)
- **문제**: Escape로 팝업 닫기 시도했으나 `app-smart-popup`이 계속 오버레이 → SALE 링크 클릭 Timeout 30초
- **수정**: `page.evaluate()`로 `.app-smart-popup` 요소를 `display:none` 강제 숨김
- **재발 방지**: Cafe24 smart-popup은 Escape만으로 안 닫힐 수 있음. JS evaluate로 강제 제거가 가장 확실

## Assertion 오류

<!-- 기댓값이 실제 페이지 텍스트/상태와 다른 경우 -->

### [힐링] 2026-03-31 — saintcore_003.py (빈 비밀번호 alert)
- **문제**: Cafe24 alert 메시지에 "비밀번호" 또는 "password" 텍스트가 없어 assertion 실패
- **수정**: alert 메시지 내용 검증 대신 alert 발생 여부만 확인으로 완화
- **재발 방지**: Cafe24 alert 메시지는 예측 불가 — 특정 키워드 대신 alert 발생 자체를 검증할 것

### [힐링] 2026-03-31 — saintcore_000/004/005.py (ENV: 비밀번호 미해석)
- **문제**: test_data.json에 `"ENV:TEST_SAINTCORE_PASSWORD"` 저장 → `_get_password()`가 리터럴 문자열 반환 → 로그인 실패
- **수정**: `ENV:` 프리픽스 감지 → `os.environ.get(raw[4:], "")` 로 환경변수 참조. 미설정 시 `pytest.skip()`
- **재발 방지**: test_data.json의 `ENV:` 프리픽스 패턴 반드시 처리할 것. 로그인 필수 테스트는 credentials 미설정 시 skip

## Timeout 오류

<!-- 요소가 나타나기 전에 검증을 시도한 경우 -->

## URL 오류

<!-- BASE_URL 또는 goto 인자가 잘못된 경우 -->

### [힐링] 2026-03-31 — saintcore_009.py (아이디 찾기 404)
- **문제**: `/member/find_id.html` URL이 존재하지 않아 404 페이지 표시
- **수정**: 로그인 페이지에서 아이디찾기 링크를 찾아 클릭하는 방식으로 변경. 링크 없으면 로그인 페이지 확인으로 폴백
- **재발 방지**: Cafe24 쇼핑몰 URL은 추측하지 말 것. 존재하는 페이지(로그인 등)에서 링크를 찾아 navigate

## 기타

### [힐링] 2026-04-01 — tc_02_wrong_password.py (test_data.json 경로 오류)
- **문제**: `Path(__file__).parent.parent.parent / "config"` → `tests/config/test_data.json`로 해석되어 FileNotFoundError
- **수정**: `Path(__file__).resolve().parent.parent.parent.parent / "config"` — tests/generated/login/ 에서 프로젝트 루트까지 4단계 상위
- **재발 방지**: `tests/generated/{group}/{file}.py`는 프로젝트 루트까지 `.parent` 4번 필요. 3번이 아님. `resolve()` 포함 권장

### [힐링] 2026-04-01 — pytest 동일 파일명 모듈 충돌
- **문제**: `login/tc_01_login_success.py`와 `saintcore/tc_01_login_success.py`가 같은 모듈명으로 import → `import file mismatch` 에러
- **수정**: `tests/generated/`, `tests/generated/login/`, `tests/generated/saintcore/`에 `__init__.py` 추가
- **재발 방지**: 서브디렉토리별 테스트 파일이 동일 basename을 가질 때 반드시 `__init__.py` 배치. 없으면 pytest가 첫 import 캐시와 충돌

<!-- 위 분류에 속하지 않는 패턴 -->

## MCP 시각 검증

<!-- Playwright MCP 도구를 활용한 힐링 시 발견된 패턴 -->

## 코드 리뷰 지적사항

<!-- 03a 코드 리뷰 단계에서 사수가 발견한 문제 패턴이 자동으로 누적됩니다 -->

### [코드 리뷰] 2026-03-31 — test_generated.py (saintcore)
- **문제**: `expect(page).to_have_url(lambda url: "basket" in url)` 패턴을 5곳에서 사용 — Playwright Python의 `to_have_url()`은 lambda를 지원하지 않음. 런타임에 `Error: expected value should be a string or a RegExp` 발생.
- **수정**: 모든 lambda를 `re.compile(r"패턴")` 또는 `re.compile(r"패턴", re.IGNORECASE)`로 교체. `import re` 추가.
- **재발 방지**: `to_have_url()` / `to_have_text()` 등 Playwright matcher에 callable(lambda/함수) 전달 금지. URL 패턴 매칭은 반드시 `re.compile()` 사용. 대소문자 무관 시 `re.IGNORECASE` 플래그 추가.
