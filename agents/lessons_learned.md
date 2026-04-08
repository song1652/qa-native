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

## Assertion 오류

<!-- 기댓값이 실제 페이지 텍스트/상태와 다른 경우 -->

## Timeout 오류

<!-- 요소가 나타나기 전에 검증을 시도한 경우 -->

## URL 오류

<!-- BASE_URL 또는 goto 인자가 잘못된 경우 -->

## 기타

<!-- 위 분류에 속하지 않는 패턴 -->

## 코드 리뷰 지적사항

<!-- 03a 코드 리뷰 단계에서 사수가 발견한 문제 패턴이 자동으로 누적됩니다 -->
