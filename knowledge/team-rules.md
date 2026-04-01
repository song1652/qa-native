# QA-Native 팀 내규

> **상태: 확정 (2026-03-31)**
> 변경 시 사용자 승인 필요.

---

## 1. 팀 구성 · 핵심 가치

> [`agents/team_charter.md`](../agents/team_charter.md) (구성·역할), [`agents/SOUL.md`](../agents/SOUL.md) (핵심 가치) 참조.

---

## 3. TC ID 규칙

### ID 구조

```
{유형}-{서비스}-{번호}
```

TC 파일 본문 상단에 메타데이터로 기록한다. 파일명은 기존 `tc_{번호}_{설명}.md` 유지.

```markdown
> TC-ID: SMK-LOGIN-001
> Priority: P0
```

### 유형 코드

| 코드 | 테스트 유형 | 설명 | 예시 |
|------|-----------|------|------|
| `SMK` | 스모크 | 핵심 기능 빠르게 확인 | `SMK-LOGIN-001` |
| `REG` | 회귀 | 기존 기능 깨짐 여부 | `REG-LOGIN-003` |
| `FNC` | 기능 | 특정 기능 상세 검증 | `FNC-CART-012` |
| `API` | API | 엔드포인트 요청/응답 검증 | `API-AUTH-005` |
| `E2E` | E2E | 사용자 시나리오 전체 흐름 | `E2E-CHECKOUT-002` |
| `SEC` | 보안 | 인증/권한/취약점 검증 | `SEC-XSS-001` |
| `PER` | 성능 | 응답시간/부하 검증 | `PER-SEARCH-001` |
| `NEG` | 네거티브 | 비정상 입력/실패 시나리오 | `NEG-LOGIN-004` |

### 서비스 코드

- 서비스명을 대문자 영문 약어로 (예: `LOGIN`, `CART`, `MYPAGE`, `CHECKOUT`)
- testcases/ 폴더명과 일치시키는 것을 권장
- 새 서비스 약어는 사수가 확인

### 번호

- 유형+서비스 조합 내에서 001부터 순번

---

## 4. 우선순위 체계 (P0~P3)

| 등급 | 명칭 | 기준 | 대응 |
|------|------|------|------|
| **P0** | Critical | 서비스 접근 불가, 핵심 기능(로그인/결제) 완전 불능 | 즉시 사용자 보고 |
| **P1** | High | 주요 기능 동작 불가, 데이터 유실 위험 | 당일 내 보고 |
| **P2** | Medium | 부분 기능 이상, UI 깨짐 (우회 가능) | 리포트에 포함 |
| **P3** | Low | 오타, 미관 이슈, 사소한 불편 | 리포트에 참고로 포함 |

---

## 5. 소통 규칙

> 말투·성격·대화 예시: [`agents/IDENTITY.md`](../agents/IDENTITY.md) 참조
> 심의 원칙·발언 규칙: [`agents/team_charter.md`](../agents/team_charter.md) 참조

---

## 6. 리뷰 체크리스트 (사수용)

TC/코드 리뷰 시 반드시 확인:

- [ ] P0 기능이 모두 커버되었는가?
- [ ] P1 기능이 90% 이상 커버되었는가?
- [ ] TC 단계가 명확하고 재현 가능한가?
- [ ] 기대결과가 구체적인가? ("정상 동작" 금지)
- [ ] 사전조건이 빠짐없이 기재되었는가?
- [ ] 엣지케이스(빈값, 특수문자, 경계값)가 고려되었는가?
- [ ] 네거티브 테스트(실패 시나리오)가 포함되었는가?
- [ ] TC ID와 Priority가 규칙에 맞게 부여되었는가?
- [ ] 셀렉터가 dom_info와 일치하는가?
- [ ] assertion이 `to_contain_text()` 등 안정적 메서드를 사용하는가?
- [ ] [`lessons_learned.md`](../agents/lessons_learned.md)의 기존 패턴이 반영되었는가?

---

## 7. 이슈 관리

### 이슈 발견 시 플로우

```
1. 테스트 실패 감지 (05_execute.py 또는 99_merge.py)
2. 힐링 루프 시도 (최대 3회)
3. 힐링 실패 시 → reports/issues/에 이슈 파일 생성
4. 심각도 판정 (P0~P3)
5. P0/P1 → 사용자에게 즉시 알림
6. P2/P3 → 리포트에 포함
```

### 이슈 파일

- 위치: `reports/issues/`
- 네이밍: `ISSUE-{YYYY-MM-DD}-{번호}.md`
- 포맷: [`templates/issue-template.md`](../templates/issue-template.md) 참조

---

## 8. 실수 대응 규칙

| 상황 | 대응 |
|------|------|
| 동일 셀렉터 오류 2회 반복 | [`lessons_learned.md`](../agents/lessons_learned.md)에 패턴 추가 |
| 동일 오류 3회 이상 | [`qa-checklist.md`](qa-checklist.md)에 항목 추가 |
| P0 이슈 발견 | 즉시 사용자에게 보고 (힐링 완료 전이라도) |
| 힐링 3회 초과 | 수동 수정 요청 + 이슈 파일 생성 |

---

## 9. 문서 관리

| 문서 유형 | 위치 | 네이밍 규칙 |
|----------|------|------------|
| 테스트케이스 | `testcases/{서비스}/` | `tc_{번호}_{설명}.md` |
| 생성된 테스트 코드 | `tests/generated/` | `test_generated.py` 또는 `{서비스}/{label}.py` |
| 테스트 리포트 | `tests/reports/` | `report_{timestamp}.html` |
| 이슈 | `reports/issues/` | `ISSUE-{YYYY-MM-DD}-{번호}.md` |
| 실수 패턴 | [`agents/lessons_learned.md`](../agents/lessons_learned.md) | (단일 파일) |
| 팀 결정사항 | [`agents/team_notes.md`](../agents/team_notes.md) | (단일 파일) |
| 토론 로그 | [`agents/dialog.json`](../agents/dialog.json) | (단일 파일) |

---

_이 문서는 2026-03-31 확정. 변경 시 사용자 승인 필요._
