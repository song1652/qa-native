# Lessons Learned — QA 자동화 실수 패턴

> **독자**: 심의 Agent — 코드 작성·리뷰·힐링 전 자동 참조.
> 같은 실수를 반복하지 않기 위한 패턴 모음.

---

## Locator 오류

- **Locator**: `expect(nav_links.first).to_be_visible(timeout=5000)` — dom_info 셀렉터 재확인, #id 우선 사용

- **Locator**: `expect(page.locator(".modal-content")).not_to_be_visible(timeout=10000)` — dom_info 셀렉터 재확인, #id 우선 사용

- **Locator**: `expect(page.locator("a[href='/category_products/4']")).to_be_visible(timeout=10000)` — dom_info 셀렉터 재확인, #id 우선 사용
- **Locator**: `expect(page.locator("h2[data-qa='account-created']")).to_be_visible(` — dom_info 셀렉터 재확인, #id 우선 사용

- **not_to_have_url 주의**: `expect(page).not_to_have_url()` 사용 시 서버가 URL을 변경하지 않는 경우 실패. 폼 제출 후 URL 변경 대신 DOM 변화(요소 소멸 등)로 검증
- **중복 셀렉터 주의**: heroku dynamic_controls 페이지는 `#loading`이 2개 존재. `#message` 텍스트 출현으로 대기할 것
- **DOM 구조 추측 금지**: heroku hovers의 캡션은 `<figcaption>` 태그가 아닌 `.figcaption` CSS 클래스. 반드시 `dom_info` 참조
- **특정 ID 존재 가정 금지**: 외부 사이트에 `#content` 등 특정 요소가 있을 거라 가정하지 말 것. URL 검증 + `body` 가시성으로 충분
- **추측 셀렉터 사용 금지**: 호스팅 플랫폼 기반 사이트는 고유 셀렉터 패턴 있음. `dom_info` 없이 `input[name='m_id']` 등 추측 금지
- **팝업 오버레이 대처**: Escape로 안 닫히는 팝업은 `page.evaluate()`로 `display:none` 강제 제거가 가장 확실

## Assertion 오류

- **Assertion**: `assert new_style != orig_style, (` — 실제 페이지 텍스트/상태로 기댓값 수정

- **Assertion**: `expect(page).to_have_url(re.compile(r"/products"), timeout=10000)` — 실제 페이지 텍스트/상태로 기댓값 수정

- **정렬 테이블 클릭 타겟**: JS 기반 정렬 테이블은 `th`가 아닌 내부 `span`/`a` 요소를 클릭. 정렬 후 DOM 업데이트 대기 필요
- **서버 에러 가능성 고려**: 외부 테스트 사이트의 특정 응답 메시지 하드코딩 금지. 폼 제출 동작 자체만 검증
- **expect() timeout 위치**: `expect(locator).to_be_visible(timeout=N)` — timeout은 matcher 메서드에 전달. `expect()` 자체에는 locator만
- **alert 메시지 검증**: 외부 사이트 alert 메시지 내용은 예측 불가. 특정 키워드 대신 alert 발생 자체를 검증
- **ENV: 프리픽스 처리**: `test_data.json`의 `ENV:` 값은 `os.environ.get()`으로 변환 필수. 미설정 시 `pytest.skip()`
- **Playwright matcher에 lambda 금지**: `to_have_url()` 등에 callable 전달 불가. URL 패턴은 `re.compile()` 사용

## URL 오류

- **URL 추측 금지**: 외부 사이트 URL 경로를 추측하지 말 것. 존재하는 페이지에서 링크를 찾아 navigate

## 광고/외부 사이트 대응

- **광고 iframe 제거 필수**: 광고가 많은 사이트(automationexercise.com 등)는 `page.goto()` 후 반드시 광고 제거: `page.evaluate("document.querySelectorAll('ins.adsbygoogle, iframe[src*=google], iframe[src*=doubleclick]').forEach(e => e.remove())")`
- **페이지 이동 후에도 광고 제거**: `page.wait_for_url()` 후에도 광고 재로드되므로 다시 제거 필요
- **scroll_into_view 광고 간섭**: `scroll_into_view_if_needed()`가 광고 때문에 실패하면 JS evaluate `el.scrollIntoView()` 사용

## 대소문자 주의

- **외부 사이트 텍스트 대소문자**: 사이트가 "All Products"인데 "ALL PRODUCTS"로 검증하면 실패. 반드시 `ignore_case=True` 옵션 사용: `expect(loc).to_contain_text("TEXT", ignore_case=True)`
- **ACCOUNT CREATED, SUBSCRIPTION 등**: automationexercise.com은 Title Case 사용. 대문자 하드코딩 금지

## strict mode 위반

- **다중 요소 셀렉터**: `a[href='/view_cart']` 등이 헤더/푸터에 중복 존재하면 strict mode 에러. `.first` 추가하거나 `.navbar-nav` 등으로 스코프 제한

## 외부 계정 의존 금지

- **existing_user 계정 의존 금지**: 외부 사이트에 특정 계정이 있다고 가정하지 말 것. 테스트 내에서 직접 회원가입 → 로그아웃 → 로그인하는 self-contained 방식 사용. 테스트 후 계정 삭제(cleanup)

## 기타

- **test_data.json 경로**: `tests/generated/{group}/{file}.py`에서 프로젝트 루트까지 `.parent` 4번 필요 (3번 아님). `resolve()` 포함 권장
- **pytest 모듈 충돌**: 서브디렉토리별 동일 basename 테스트 파일이 있으면 `__init__.py` 필수
- **navigate 중 evaluate 금지**: 클릭 후 페이지 이동이 예상되면 `wait_for_load_state()` 호출 후 evaluate. 팝업 제거는 try/except 처리
- **HTML5 validation 가정 금지**: 외부 사이트의 input에 `required` 속성이 있을 거라 가정하지 말 것. `checkValidity()` 대신 실제 제출 후 응답으로 검증

## 셀렉터 정확도 개선

- **서브페이지 DOM 확인 필수**: 메인 URL만 분석하면 inputs=0, buttons=0. testcases/*.md의 steps에서 서브페이지 URL을 추출하여 각각 DOM 분석 필요
- **to_have_class에 re.compile 필수**: 문자열 regex `r".*active.*"` 는 작동하지 않음. `re.compile(r"active")` 사용
- **중복 ID 주의**: droppable 등 탭 구조에서 동일 ID가 여러 pane에 존재 → 활성 pane으로 스코핑 필수
- **progress bar 컨테이너 구분**: `#progressBar`가 `.progress` 컨테이너일 수 있음. 실제 바는 `#progressBar .progress-bar`
- **triple_click 없음**: Playwright Python에 없는 메서드. `click(click_count=3)` 사용

## 테이블 정렬 검증

- **정렬 데이터 비교 대신 CSS 클래스 검증**: tablesorter 테이블은 클릭 후 데이터가 정렬되지만, 읽기 시점에 아직 미반영될 수 있음. `headerSortUp`/`headerSortDown` CSS 클래스 적용 여부로 검증이 더 안정적
- **정렬 컬럼 클릭 대상**: `th` 직접 클릭이 `th > span` 클릭보다 확실. span이 존재하지 않는 테이블도 있음

## Enter 키와 폼 제출

- **Enter 키가 폼 제출 트리거**: input 필드에서 Enter 누르면 form submit 발생하여 페이지 리로드됨. `#result` 텍스트가 순간 표시 후 사라짐. `page.evaluate()`로 form submit 이벤트를 `preventDefault()` 처리 후 키 입력

## Shadow DOM 접근

- **Shadow DOM 텍스트 추출**: Playwright의 일반 locator로 shadow DOM 내부 접근 불가. `page.evaluate()`로 `el.shadowRoot.textContent` 직접 읽기. CSS style 태그 내용도 포함되므로 실제 텍스트 확인 필수
- **Shadow DOM 실제 콘텐츠 확인**: the-internet.herokuapp.com/shadowdom의 첫 번째 요소는 "My default text", 두 번째는 리스트 항목. "Let's have some different text!"는 존재하지 않음

## TinyMCE 에디터

- **TinyMCE 오버레이 방해**: TinyMCE 에디터의 toolbar/overlay가 `#tinymce` body 클릭을 가로챔. `editor.click()` + `editor.fill()` 대신 `page.evaluate()`로 `iframe.contentDocument.querySelector('#tinymce').innerHTML` 직접 설정

## 사라지는 요소 (Disappearing Elements)

- **Gallery 링크 비결정적**: heroku /disappearing_elements 페이지의 "Gallery" 링크는 랜덤으로 나타남/사라짐. nav 링크 수 검증은 `>= 4` (5 아님)

## 코드 생성 시 lint 오류

- **미사용 import 금지**: `import re`, `from playwright.sync_api import expect` 등 실제 코드에서 사용하지 않는 모듈을 import하면 F401 lint 오류. 코드 완성 시 사용하는 모듈만 import할 것
- **미사용 변수 금지**: `old_text = button.inner_text()` 등 할당만 하고 참조하지 않으면 F841. 불필요한 변수 할당 제거

## Timeout 오류

- **Timeout**: `E   playwright._impl._errors.TimeoutError: Timeout 30000ms exceeded.` — expect(..., timeout=10000) 또는 wait_for_selector 추가
- **Timeout**: `E   playwright._impl._errors.TimeoutError: Timeout 30000ms exceeded.` — expect(..., timeout=10000) 또는 wait_for_selector 추가

- **Timeout**: `async with self.expect_navigation(` — expect(..., timeout=10000) 또는 wait_for_selector 추가
