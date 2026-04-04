# 코드 리뷰 심의 프롬프트 (03a_dialog.py 후 사용)

> 이 파일은 심의 Agent에 대한 행동 지침이다.
> `{ctx.*}` 참조는 DELIBERATION_CONTEXT JSON의 해당 키를 의미한다.
> Playwright 코드 규칙: `.claude/skills/playwright-best-practices/SKILL.md` 참조.

아래 컨텍스트를 바탕으로 코드 리뷰를 수행하고 필요 시 코드를 직접 수정하라.

team_charter: {ctx.team_charter}
generated_code: {ctx.generated_code}
lint_result: {ctx.lint_result}
plan: {ctx.plan}

수행할 작업:
1. lint 이슈 수정 (있는 경우 해당 tests/generated/{group}/*.py 파일 직접 편집)
2. `.claude/skills/playwright-best-practices/SKILL.md` 기준으로 셀렉터/assertion 검토
3. state/pipeline.json에 review_summary 저장, step = "reviewed"
4. 리뷰 중 발견된 새로운 실수 패턴이 있으면 agents/lessons_learned.md 해당 섹션에 한 줄 패턴으로 추가 (기존 패턴과 중복 시 생략)

## 필수 검토 항목
- 공유 헬퍼 금지: helpers.py 등 외부 파일 import -> 각 파일 자체 완결
- test_data 경로: `Path(__file__).resolve().parent` 4번 -> 프로젝트 루트 (3번 아님)
- 함수명 영문: `test_{english_snake_case}` 형식 (한글 금지)
- ENV: 프리픽스: `os.environ.get()` 처리, 미설정 시 `pytest.skip()`
- 그 외 Playwright 코드 규칙은 SKILL.md 참조
