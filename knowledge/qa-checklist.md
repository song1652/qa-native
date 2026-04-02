# QA 체크리스트

> 스모크 테스트 항목 가이드 + Playwright 테스트 작성 체크리스트

---

## 웹 서비스 스모크 항목

- [ ] 메인 페이지 로딩
- [ ] 로그인/로그아웃
- [ ] 회원가입 (있는 경우)
- [ ] 핵심 페이지 네비게이션
- [ ] 주요 CRUD 기능 (생성/조회/수정/삭제)
- [ ] 검색 기능
- [ ] 권한별 접근 제어

## API 스모크 항목

- [ ] 헬스체크 엔드포인트
- [ ] 인증 API (로그인/토큰 발급)
- [ ] 주요 GET 엔드포인트 응답 확인
- [ ] 주요 POST 엔드포인트 정상 처리
- [ ] 에러 응답 형식 (4xx, 5xx)

## 배포 후 확인 항목

- [ ] SSL 인증서 유효
- [ ] 리다이렉트 정상 동작
- [ ] 정적 리소스 로딩 (이미지, CSS, JS)
- [ ] 콘솔 에러 없음
- [ ] API 응답 시간 정상 범위

---

## Playwright 테스트 작성 체크리스트

### 셀렉터

- [ ] `#id` 셀렉터 우선 사용
- [ ] id 없으면 `[name=...]`, `[data-testid=...]` 순서로 선택
- [ ] DOM 분석(dom_info) 결과와 셀렉터 일치 확인
- [ ] 추측한 셀렉터 없음 — 모두 dom_info 기반

### Assertion

- [ ] `expect()` 사용 (vanilla assert 금지)
- [ ] `to_contain_text()` 사용 (`to_have_text()`는 공백 문제 위험)
- [ ] URL 검증 시 `re.compile()` 사용 (lambda 금지)
- [ ] 구체적 텍스트/상태를 기대값으로 지정 ("정상 동작" 금지)

### 코드 구조

> 상세: [`CLAUDE.md`](../CLAUDE.md) "절대 규칙" + [`prompts/parallel_subagent.md`](../prompts/parallel_subagent.md) 참조

### 안정성

- [ ] 팝업/오버레이 차단 처리 (필요 시 `page.evaluate()`)
- [ ] `page.wait_for_selector()` 또는 `expect(locator).to_be_visible(timeout=N)` 적절히 사용
- [ ] `expect()` 호출 시 timeout은 matcher 메서드에 전달 (`expect(loc, timeout=N)` 금지)
- [ ] alert 처리 시 내용 대신 발생 여부만 검증 (사이트별 메시지 다를 수 있음)
- [ ] 환경변수 계정 (`ENV:` prefix) 누락 시 `pytest.skip()` 처리

### MCP 시각 검증 (힐링 시)

- [ ] 실패 스크린샷은 최종 실패 시만 저장 (힐링 중간 실행 시 매번 초기화)
- [ ] 스크린샷 위치: `tests/screenshots/{group}__{name}.png`
- [ ] heal_context에 screenshot 경로 포함 확인
- [ ] Locator 오류 시 Playwright MCP로 실제 DOM 셀렉터 확인
- [ ] Assertion 오류 시 Read tool로 스크린샷 시각 확인
- [ ] MCP 브라우저 세션은 pytest와 별개임을 인지 (쿠키 비공유)
