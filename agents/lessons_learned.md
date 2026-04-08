# Lessons Learned — QA 자동화 실수 패턴

> **독자**: 심의 Agent — 코드 작성·리뷰·힐링 전 자동 참조.
> 같은 실수를 반복하지 않기 위한 **큐레이션된** 패턴 모음.
> 자동 기록 로그는 [lessons_learned_auto.md](lessons_learned_auto.md) 참조.

---

## Locator 오류

- **not_to_have_url 주의**: `expect(page).not_to_have_url()` 사용 시 서버가 URL을 변경하지 않는 경우 실패. 폼 제출 후 URL 변경 대신 DOM 변화(요소 소멸 등)로 검증
- **중복 셀렉터 주의**: heroku dynamic_controls 페이지는 `#loading`이 2개 존재. `#message` 텍스트 출현으로 대기할 것
- **DOM 구조 추측 금지**: heroku hovers의 캡션은 `<figcaption>` 태그가 아닌 `.figcaption` CSS 클래스. 반드시 `dom_info` 참조
- **hover는 page.hover() 대신 locator().hover()**: `page.hover("div.figure:nth-child(N)")` 방식은 :nth-child 선택이 컨테이너 context 없이 실패 가능. `page.locator("div.figure").nth(N).hover()` 패턴 사용
- **dynamic_controls 재추가 후 #checkbox는 input 자체**: 최초 상태는 `#checkbox div` > `input`, 재추가 후 `#checkbox`가 input element. `#checkbox input` 셀렉터 불가 → `#checkbox-example input[type=checkbox]` 사용
- **shadow DOM textContent는 CSS 포함**: `shadowRoot.textContent`는 style 태그 내 CSS 텍스트까지 포함. slot 내용 검증은 `element.innerText` 또는 `element.textContent`(light DOM) 사용
- **shadowRoot.innerText는 undefined**: `shadowRoot`에 `innerText` 프로퍼티 없음. `shadowRoot.textContent` 사용 (CSS 포함 감수)
- **shadow DOM nth-of-type vs querySelectorAll**: `my-paragraph:nth-of-type(2)` 셀렉터가 작동 안 할 수 있음. `document.querySelectorAll('my-paragraph')[1]`로 인덱스 접근
- **특정 ID 존재 가정 금지**: 외부 사이트에 `#content` 등 특정 요소가 있을 거라 가정하지 말 것. URL 검증 + `body` 가시성으로 충분
- **추측 셀렉터 사용 금지**: 호스팅 플랫폼 기반 사이트는 고유 셀렉터 패턴 있음. `dom_info` 없이 `input[name='m_id']` 등 추측 금지
- **팝업 오버레이 대처**: Escape로 안 닫히는 팝업은 `page.evaluate()`로 `display:none` 강제 제거가 가장 확실

## Assertion 오류

- **tablesorter 첫 클릭은 headerSortDown**: `th` 첫 클릭 시 `headerSortDown` 적용, 두 번째 클릭 시 `headerSortUp`. `headerSortUp` 단독 검증이 필요하면 두 번 클릭할 것. 클릭 후 `page.wait_for_timeout(300)` 대기 필수
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

- **test_data.json 그룹 키 필수**: `test_data["heroku"]["forgot_email"]` 처럼 그룹 키 포함하여 접근. KeyError 방지
- **page.evaluate()에 arrow function 필수**: return 문 사용 시 반드시 `() => { ... }` 래핑. 직접 return 사용 시 SyntaxError
- **drag-and-drop JS 시뮬레이션**: `new DragEvent()`는 the-internet.herokuapp.com에서 동작 안 함. CustomEvent + `initCustomEvent()` + dataTransfer 객체 수동 주입 방식 사용
- **동적 콘텐츠 exact count 금지**: dynamic_content 등 서버 응답이 가변적인 페이지는 `to_have_count(3)` 대신 `count >= 1`로 검증
- **download href 형식**: the-internet.herokuapp.com/download 링크 href는 `/download/filename` 아닌 `download/filename` (상대 경로). `"/download/" in href` 대신 `"download" in href` 사용
- **floating_menu CSS position**: the-internet.herokuapp.com/floating_menu의 #menu는 `position: absolute` (fixed 아님). CSS position 검증 대신 뷰포트 내 visible 여부로 검증
- **geolocation grant_permissions asyncio 충돌**: `context.grant_permissions(["geolocation"])` 사용 시 asyncio loop 에러 발생 가능. `page.evaluate()`로 `navigator.geolocation.getCurrentPosition`을 직접 모킹하는 방식 사용
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

## heroku 힐링 패턴 (2026-04-06)

- **drag-and-drop DragEvent 방식**: `CustomEvent + initCustomEvent()` 방식은 column-b를 "undefined"로 만듦. `document.createEvent('DragEvent') + initEvent() + Object.defineProperty(e, 'dataTransfer', {value: dt})` 방식 사용
- **exit intent 모달**: `#modal` 셀렉터 없음, 실제는 `#ouibounce-modal`. 마우스 이벤트로 트리거 안 됨 → `_ouibounce.fire()` 직접 호출
- **floating menu viewport 체크 금지**: `position: absolute`이므로 스크롤 후 `rect.top < 0`. 뷰포트 좌표 검증 대신 DOM 존재 + 링크 포함 여부로 검증
- **jqueryui menu get_by_role 금지**: 서브메뉴 항목은 hover 전까지 `display:none`. `get_by_role("menuitem", name=...)` 불가 → `page.locator("#menu > li.ui-menu-item").nth(1).hover()` 후 `page.locator("#menu a", has_text=...)` 사용. nth(0)은 "Disabled", nth(1)이 "Enabled"
- **JS 에러 감지는 pageerror 이벤트**: `page.on("console")` + `msg.type == "error"`는 JS 런타임 에러를 잡지 못함. `page.on("pageerror", handler)` 사용
- **jqueryui PDF 클릭**: PDF 링크는 파일 다운로드 → `net::ERR_ABORTED` 발생. `expect_navigation` 대신 href 속성 검증
- **shadow DOM 두 번째 요소**: `shadowRoot.textContent`에 CSS 스타일 포함. 실제 slot 내용은 host element의 `innerHTML`에서 확인
- **shifting content list**: `<li>` 없음, `<br><br>` 구분 텍스트. `li` 셀렉터 대신 `.large-6` 컨텐츠 영역 텍스트 검증
- **shifting content image strict mode**: `locator("img")`가 2개 반환(GitHub badge + content img) → `#content img.shift`로 스코핑
- **TinyMCE 6+ 셀렉터**: `iframe#mce_0_ifr` 없음, 실제는 `iframe.tox-edit-area__iframe`. toolbar는 `.tox-editor-header`
- **dropdown option[disabled] to_be_visible 실패**: `<option>` 요소는 Playwright에서 hidden 처리. `to_be_visible()` 대신 `.count() > 0` + JS `selectedIndex` 텍스트 검증
- **dynamic content strict mode**: row 0은 레이아웃 헤더 행(img 3개), row 1-3이 실제 콘텐츠. `img.first` 없이 `row.locator("img")`는 strict mode 위반 → row별 img count 검사 후 처리

## demoqa.com 추가 패턴 (2026-04-06)

- **alert 버튼 locator**: `get_by_role("button", name="...")` 대신 ID 사용 — `#alertButton`, `#timerAlertButton`, `#confirmButton`, `#promtButton` (promtButton 오타 주의)
- **modal Close 버튼**: `get_by_role("button", name="Close")` strict mode 위반 (x 버튼 + Close 버튼 2개). ID 사용: `#closeSmallModal`, `#closeLargeModal`
- **webtable rows select**: 옵션 value="10"/"20"/"30"/"40"/"50". "5 rows"/"10 rows" 라벨 없음
- **droppable "Drop Here"**: 텍스트가 "Drop Here" (대문자 H). "Drop here" 아님
- **droppable prevent propagation 탭 ID**: `#droppableExample-tab-preventPropogation` (오타 Propogation)
- **dragabble container**: `.draggable-parent` 없음 → `.containment-wrapper`. 내부 드래그 요소는 `.draggable`
- **react-select singleValue**: CSS module 동적 클래스 → JS evaluate로 `[class*="singleValue"]` 접근
- **#cars**: 일반 `<select multiple>`. `select_option(["volvo","saab"])` 사용
- **menu "SUB SUB LIST"**: 텍스트에 `»` 포함 → `locator("a").filter(has_text="SUB SUB LIST")` 사용
- **menu "Sub Item"**: 2개 존재 → `.first` 추가 필수
- **form 라디오/체크박스 label**: `has_text` strict mode 위반 가능. `label[for='gender-radio-1']` 방식으로 특정
- **form empty submit 검증**: `field-error` 클래스 없음 → 모달 비표시 + 빈 필드 값으로 검증
- **sidebar header**: `.main-header` 없음 → `.text-center` 사용
- **dynamic-properties 버튼**: "Will react on click" 없음 → `#enableAfter` disabled→enabled 전환 검증
- **locator.wait_for(state="enabled")**: 지원 안 됨 → `expect(locator).to_be_enabled(timeout=N)` 사용

## demoqa.com 사이트 구조 변경 (2026-04-06)

- **networkidle 금지**: demoqa.com은 광고 스크립트가 많아 `wait_for_load_state("networkidle")`가 30초 이상 걸려 타임아웃. `"domcontentloaded"` + `wait_for_timeout(2000)` 사용
- **rc-tree (체크박스)**: 구 `rct-*` 클래스가 `rc-tree-*`로 변경. 확장: `.rc-tree-switcher_close` 클릭, 축소: `.rc-tree-switcher_open` 클릭, 체크박스: `.rc-tree-checkbox[aria-label='Select {name}']`, 제목: `.rc-tree-title`. 별도 expand-all/collapse-all 버튼 없음
- **웹 테이블**: 구 `rt-table`/`rt-tbody`/`rt-tr-group` 대신 표준 `<table>`/`<tbody>`/`<tr>`/`<td>`. 페이지당 행 수 select는 `select.form-control`(옵션: "Show 10", "Show 20" 등). 헤더 클릭 정렬 미지원
- **아코디언**: 구 `#section1Heading`/`#section1Content` 대신 Bootstrap 5 `.accordion-item` > `.accordion-button` + `.accordion-body`
- **드롭 가능(accept 탭)**: `#notAcceptable` ID 없어짐. "Not Acceptable" 텍스트로 `.drag-box` 찾기. drop 영역은 `.drop-box` (ID 없음)
- **폼 모달 닫기**: `#closeLargeModal` 버튼 클릭 불작동. `page.keyboard.press("Escape")` 사용
- **jQuery UI drag**: `drag_to()` 및 `page.mouse.move()` 불안정. JS `dispatchEvent(new MouseEvent())` 방식이 가장 안정적: mousedown → mousemove(20 steps) → mouseup. footer/광고 제거 선행 필수
- **react-select subjects**: Enter 키가 폼 전체를 submit함. 옵션 드롭다운 `.subjects-auto-complete__option` 클릭 사용
- **resizable handle**: footer와 광고가 pointer events 가로챔. footer 포함 모든 overlay 제거 후 드래그
