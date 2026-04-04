# 힐링 패치 기준

모든 파이프라인(단일/병렬)에서 힐링 시 동일 기준 적용:

| 오류 유형 | 판별 키워드 | 패치 방법 |
|-----------|------------|-----------|
| Locator | `strict mode violation`, `Element not found` | dom_info 셀렉터와 대조해 수정 |
| Assertion | `Expected ... to contain` | 실제 페이지 텍스트를 기댓값으로 수정 |
| Timeout | `Timeout` | `page.wait_for_selector()` 추가 또는 `expect(..., timeout=10000)` 조정 |
| URL | `goto`, `navigation` | BASE_URL 또는 goto 인자 수정 |

## [필수] 힐링 완료 체크리스트

하나라도 빠지면 힐링 미완료:

1. 코드 패치 적용
2. `agents/lessons_learned.md`에 한 줄 패턴 형식으로 기록 (이미 같은 패턴이 있으면 생략):
   ```
   - **{핵심 키워드}**: {상황 설명}. {해결법/교훈}
   ```
3. 재실행으로 통과 확인

## MCP 시각 검증 (힐링 시 선택 사용)

traceback만으로 원인이 불명확한 Locator/Assertion/Timeout 오류에만 사용한다.
heal_context의 각 failure에 `screenshot` 경로가 포함되어 있으면 활용 가능.

1. **스크린샷 확인**: Read tool로 `heal_context.failures[].screenshot.path` 파일 열기 → 실패 시점 화면 확인
2. **실제 페이지 탐색** (필요 시만):
   - `Playwright_navigate` → heal_context의 URL로 접속
   - `playwright_get_visible_html` → 현재 페이지 DOM 구조 확인
   - `playwright_get_visible_text` → 현재 페이지 텍스트 확인
3. **셀렉터 검증** (필요 시만):
   - `Playwright_evaluate` → `document.querySelector('셀렉터')` 로 셀렉터 존재 확인
4. **패치 적용**: 시각 검증 결과를 바탕으로 테스트 코드 수정

**주의사항**:
- MCP 도구는 힐링 경로에서만 사용 (정상 실행 시 사용 금지 → 비용 절감)
- MCP 브라우저와 pytest 브라우저는 별개 세션이므로 쿠키/상태가 공유되지 않는다
- 로그인 등 전제조건이 필요한 페이지는 DOM/텍스트 확인에 그친다
