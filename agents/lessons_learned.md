# Lessons Learned — QA 자동화 실수 패턴

> **독자**: 심의 Agent — 코드 작성·리뷰·힐링 전 자동 참조.
> 같은 실수를 반복하지 않기 위한 패턴 모음.

---

## Locator 오류

- **중복 셀렉터 주의**: heroku dynamic_controls 페이지는 `#loading`이 2개 존재. `#message` 텍스트 출현으로 대기할 것
- **DOM 구조 추측 금지**: heroku hovers의 캡션은 `<figcaption>` 태그가 아닌 `.figcaption` CSS 클래스. 반드시 `dom_info` 참조
- **특정 ID 존재 가정 금지**: 외부 사이트에 `#content` 등 특정 요소가 있을 거라 가정하지 말 것. URL 검증 + `body` 가시성으로 충분
- **추측 셀렉터 사용 금지**: 호스팅 플랫폼 기반 사이트는 고유 셀렉터 패턴 있음. `dom_info` 없이 `input[name='m_id']` 등 추측 금지
- **팝업 오버레이 대처**: Escape로 안 닫히는 팝업은 `page.evaluate()`로 `display:none` 강제 제거가 가장 확실

## Assertion 오류

- **정렬 테이블 클릭 타겟**: JS 기반 정렬 테이블은 `th`가 아닌 내부 `span`/`a` 요소를 클릭. 정렬 후 DOM 업데이트 대기 필요
- **서버 에러 가능성 고려**: 외부 테스트 사이트의 특정 응답 메시지 하드코딩 금지. 폼 제출 동작 자체만 검증
- **expect() timeout 위치**: `expect(locator).to_be_visible(timeout=N)` — timeout은 matcher 메서드에 전달. `expect()` 자체에는 locator만
- **alert 메시지 검증**: 외부 사이트 alert 메시지 내용은 예측 불가. 특정 키워드 대신 alert 발생 자체를 검증
- **ENV: 프리픽스 처리**: `test_data.json`의 `ENV:` 값은 `os.environ.get()`으로 변환 필수. 미설정 시 `pytest.skip()`
- **Playwright matcher에 lambda 금지**: `to_have_url()` 등에 callable 전달 불가. URL 패턴은 `re.compile()` 사용

## URL 오류

- **URL 추측 금지**: 외부 사이트 URL 경로를 추측하지 말 것. 존재하는 페이지에서 링크를 찾아 navigate

## 기타

- **test_data.json 경로**: `tests/generated/{group}/{file}.py`에서 프로젝트 루트까지 `.parent` 4번 필요 (3번 아님). `resolve()` 포함 권장
- **pytest 모듈 충돌**: 서브디렉토리별 동일 basename 테스트 파일이 있으면 `__init__.py` 필수
- **navigate 중 evaluate 금지**: 클릭 후 페이지 이동이 예상되면 `wait_for_load_state()` 호출 후 evaluate. 팝업 제거는 try/except 처리
