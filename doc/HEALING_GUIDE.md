# 힐링 가이드

모든 파이프라인(단일/병렬)에서 힐링 시 동일 기준 적용.

> 오류 유형별 패치 전략 상세: `.claude/skills/heal-patterns/SKILL.md`
> Playwright 코드 작성 베스트프랙티스: `.claude/skills/playwright-best-practices/SKILL.md`

## [필수] 힐링 완료 체크리스트

하나라도 빠지면 힐링 미완료:

1. 코드 패치 적용
2. `agents/lessons_learned.md`에 한 줄 패턴 형식으로 기록 (`heal_utils.py`가 중복 자동 건너뜀):
   ```
   - **{핵심 키워드}**: {상황 설명}. {해결법/교훈}
   ```
3. 재실행으로 통과 확인

## 힐링 제한 및 재실행 옵션

**최대 3회 제한**: 06_heal.py가 자동으로 `heal_count` 추적. 초과 시 `step = "heal_failed"`, 종료코드 2로 중단.

**--only-failed 옵션**: 이전 실행 결과의 실패 테스트만 선택적으로 재실행
```bash
python scripts/05_execute.py --only-failed [--no-report]
```
- 성공한 테스트는 건너뜀
- 힐링 중간 재실행 속도 향상 (불필요한 테스트 제외)
- 전체 통과 후 최종 실행 시에는 전체 재실행 권장

## 빈도 데이터 활용

- `06_heal.py`가 실패 시 `state/heal_stats.json`에 오류 패턴별 빈도 자동 기록
- `06a_dialog.py`가 Top 5 빈출 패턴을 DELIBERATION_CONTEXT에 자동 주입
- 빈출 패턴은 힐링 시 우선 점검 대상

## OMC ultraqa를 이용한 자동 힐링

손수 패치하는 대신 `/oh-my-claudecode:ultraqa` 스킬로 자동 힐링 가능:

```
python scripts/05_execute.py --no-report
(실패 발생 시)
/oh-my-claudecode:ultraqa
  - 목표: 실패 테스트 자동 분석 후 패치 + 재실행
  - 최대 3회까지 자동 반복 (초과 시 중단)
  - 명령: .venv/bin/python -m pytest tests/generated/{group}/ -n 8 --tb=short
```

**주의**: ultraqa는 최대 3회 제한을 추적하므로, 3회 초과 실패는 수동 개입 필요.

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
