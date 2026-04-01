# 코드 리뷰 심의 프롬프트 (03a_dialog.py 후 사용)

아래 컨텍스트를 바탕으로 코드 리뷰를 수행하고 필요 시 코드를 직접 수정하라.

team_charter: {ctx.team_charter}
generated_code: {ctx.generated_code}
lint_result: {ctx.lint_result}
plan: {ctx.plan}

수행할 작업:
1. lint 이슈 수정 (있는 경우 tests/generated/test_generated.py 직접 편집)
2. 셀렉터·assertion 검토 후 개선 사항 반영
3. state/pipeline.json에 review_summary 저장, step = "reviewed"
4. 리뷰 중 발견된 문제점이 있으면 agents/lessons_learned.md 해당 섹션에 추가

## 필수 검토 항목 (CLAUDE.md 발췌)
- **lambda 금지**: `to_have_url()`, `to_have_text()` 등에 lambda/callable 전달 → `re.compile()` 필수
- **공유 헬퍼 금지**: helpers.py 등 외부 파일 import → 각 파일 자체 완결
- **test_data 경로**: `Path(__file__).resolve().parent` 4번 → 프로젝트 루트 (3번 아님)
- **함수명 영문**: `test_{english_snake_case}` 형식 (한글 금지)
- **ENV: 프리픽스**: `os.environ.get()` 처리, 미설정 시 `pytest.skip()`
   형식 (발견 사항 없으면 생략):
   ```
   ### [코드 리뷰] {날짜} — {테스트 파일}
   - **문제**: {발견된 문제 내용}
   - **수정**: {적용한 수정 내용}
   - **재발 방지**: {동일 실수를 피하기 위한 규칙}
   ```
