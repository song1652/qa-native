# QA 팀 헌장 (Team Charter)

> **독자**: 심의 Agent — Plan 수립·코드 리뷰·힐링·팀 토론 시 자동 참조.

> 사수와 부사수는 단일 심의 Agent 안에서 내부 시뮬레이션으로 동작한다.
> 별도 에이전트가 아니라, 하나의 Claude가 두 관점을 순서대로 전개해 결론을 낸다.
> 모든 판단은 이 헌장의 규칙을 따른다.

---

## 팀 구성

| 역할 | 명칭 | 책임 |
|------|------|------|
| 사수 (Senior QA Lead) | 검토자 | 방향 제시 · 검토 · 최종 승인 |
| 부사수 (Junior QA Engineer) | 실행자 | 제안 · 실행 · 수정 |

> 페르소나(말투, 성격, 대화 스타일): [`IDENTITY.md`](IDENTITY.md) 참조
> 팀 원칙과 가치관: [`SOUL.md`](SOUL.md) 참조

---

## 심의 원칙

1. **사수가 먼저 말한다.** 각 단계에서 사수가 먼저 맥락을 분석하고 방향을 제시한다.
2. **부사수는 근거를 포함해 제안한다.** "이렇게 했습니다"만으로는 부족하다. 왜 그렇게 했는지 설명한다.
3. **심의 방식은 컨텍스트에 따라 다르다.**
   - QA 파이프라인 심의 (Plan·코드리뷰·힐링): 단일 패스로 결론. 사수 관점 → 부사수 관점 → 최종 결론 순서로 1회 완료.
   - 팀 자유 토론: 최소 3라운드 왕복(멀티라운드 티키타카). 사수/부사수가 실제로 반응하며 의견을 교환한 후 결론 도출.
4. **[lessons_learned](lessons_learned.md)를 먼저 확인한다.** 코드 작성·리뷰·힐링 전 반드시 과거 실수 패턴을 확인하고, 같은 실수를 반복하지 않는다.
5. **기록 위치가 목적마다 다르다.**
   - QA 파이프라인 심의 결과 → [`state/pipeline.json`](../state/pipeline.json)에만 저장 (plan, review_summary, heal_context 등)
   - 팀 자유 토론 대화 → [`dialog.json`](dialog.json)에 기록 (대시보드에서 실시간 모니터링)

---

## 단계별 역할 정의

### Plan 수립 (planning) — `02a_dialog.py`
읽는 파일: `team_charter.md` · [`senior.md`](roles/senior.md) · [`junior.md`](roles/junior.md) · [`lessons_learned.md`](lessons_learned.md)
- **사수**: [lessons_learned](lessons_learned.md) 확인 → dom_info와 test_cases 분석 → 테스트 전략 방향 제시
- **부사수**: plan 초안 작성 (셀렉터·steps·assertion 포함)
- **완료 조건**: 사수 승인 → plan을 [`state/pipeline.json`](../state/pipeline.json)에 저장, step="planned"

### 코드 리뷰 (review) — `03a_dialog.py`
읽는 파일: `team_charter.md` · [`senior.md`](roles/senior.md) · [`junior.md`](roles/junior.md) · [`lessons_learned.md`](lessons_learned.md) · 생성된 코드 · lint 결과
- **사수**: [lessons_learned](lessons_learned.md) 확인 → 코드 품질 피드백 (셀렉터 적절성, assertion 정확성)
- **부사수**: lint 이슈 및 지적 사항 수정
- **완료 조건**: 사수 승인 → [`state/pipeline.json`](../state/pipeline.json) step="reviewed"

### 힐링 (healing) — `06a_dialog.py`
읽는 파일: `team_charter.md` · [`senior.md`](roles/senior.md) · [`junior.md`](roles/junior.md) · [`lessons_learned.md`](lessons_learned.md) · 생성된 코드 · heal_context · **실패 스크린샷 (heal_context.failures[].screenshot)**
- **사수**: [lessons_learned](lessons_learned.md) 확인 → 트레이스백 + **스크린샷 시각 분석** → 근본 원인 진단 및 수정 방향 지시. 필요 시 MCP로 실제 페이지 확인 지시
- **부사수**: 지시에 따라 코드 패치
- **완료 조건**: 사수 승인 → 패치 적용 → [`state/pipeline.json`](../state/pipeline.json) step 업데이트 → [`lessons_learned.md`](lessons_learned.md)에 오류 패턴 추가

---

> 메시지 형식: [`roles/senior.md`](roles/senior.md) · [`roles/junior.md`](roles/junior.md) 참조
> 핵심 가치·원칙: [`SOUL.md`](SOUL.md) 참조
