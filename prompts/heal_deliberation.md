# 힐링 심의 프롬프트 (06a_dialog.py 후 사용)

아래 컨텍스트를 바탕으로 실패를 진단하고 코드를 직접 패치하라.

generated_code: {ctx.generated_code}
heal_context: {ctx.heal_context}
dom_info: {ctx.dom_info}

수행할 작업:
1. 각 failure의 traceback 분석 → 오류 유형 분류 (Locator/Assertion/Timeout/URL)
2. tests/generated/test_generated.py 직접 패치 (공통 힐링 패치 기준 참조)
3. **[필수]** agents/lessons_learned.md에 힐링 기록 (누락 시 99_merge.py가 경고)
4. heal_context에 screenshot 경로가 있으면 Read tool로 시각 확인
5. traceback만으로 원인 불명확 시 MCP 시각 검증 절차 참조

## 힐링 완료 체크리스트 (하나라도 빠지면 미완료)
1. 코드 패치 적용
2. agents/lessons_learned.md에 기록:
   ```
   ### [힐링] {날짜} — {파일명}
   - **문제**: {traceback 요약}
   - **수정**: {적용한 패치 내용}
   - **재발 방지**: {동일 실수 방지 규칙}
   ```
3. 재실행으로 통과 확인

## 핵심 패치 규칙
- Locator 오류: dom_info 셀렉터와 대조해 수정
- Assertion 오류: 실제 페이지 텍스트를 기댓값으로 수정
- Timeout 오류: `page.wait_for_selector()` 추가 또는 `expect(..., timeout=10000)` 조정
- URL 오류: BASE_URL 또는 goto 인자 수정
- lambda/callable → `re.compile()` 교체 (Playwright matcher에 lambda 전달 금지)
