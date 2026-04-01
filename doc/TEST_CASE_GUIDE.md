# QA-Native 테스트 케이스 작성 가이드

> **독자**: 사람 — 테스트케이스 작성 규칙. 에이전트가 읽지 않음.

QA-Native 파이프라인용 테스트 케이스 작성 가이드입니다.
모든 케이스 파일은 이 가이드를 따라 일관성 있게 작성되어야 합니다.

---

## 파일 규칙

- **형식**: Markdown (`.md`)
- **위치**: `testcases/{그룹명}/tc_{번호}_{설명}.md`
- **1파일 = 1케이스**: 파일 하나에 테스트 케이스 하나
- **그룹명**: 기능 단위 폴더 (예: `login`, `mypage`, `signup`)
- **템플릿**: [`templates/tc-template.md`](../templates/tc-template.md) 참조

```
testcases/
  login/
    tc_01_login_success.md
    tc_02_wrong_password.md
    tc_03_empty_username.md
  mypage/
    tc_01_profile_view.md
```

---

## 케이스 파일 형식

YAML frontmatter + Markdown 본문으로 구성한다.

```markdown
---
id: tc_01
data_key: valid_user
priority: high
tags: [positive, smoke]
type: structured
---
# 케이스 제목

## Precondition
0. 시작 조건

## Steps
1. username 필드에 test_data[valid_user].username 입력
2. password 필드에 test_data[valid_user].password 입력
3. Login 버튼 클릭

## Expected
- 기대 결과
```

---

## Frontmatter 필드

파일 최상단 `---` 블록 안에 메타데이터를 기록한다.

| 필드 | 필수 | 값 | 설명 |
|------|------|-----|------|
| `id` | **필수** | `tc_{번호}` | 케이스 고유 식별자 (그룹 내 순번) |
| `data_key` | **필수** | [`test_data.json`](../config/test_data.json) 키 \| `null` | 입력값 참조 키. 입력 불필요 시 `null` |
| `priority` | **필수** | `high` \| `medium` \| `low` | 우선순위 |
| `tags` | **필수** | 배열 `[유형, 분류]` | 테스트 유형 태그 |
| `type` | **필수** | `structured` \| `natural` | 케이스 형식 |

### 유형 태그 (tags)

| 태그 | 설명 |
|------|------|
| `positive` | 정상 동작 확인 |
| `negative` | 비정상 입력/실패 시나리오 |
| `smoke` | 핵심 기능 빠르게 확인 |
| `auth` | 인증/로그인 관련 |
| `validation` | 입력값 검증 |
| `security` | 보안 취약점 확인 |
| `edge_case` | 경계값/특수 상황 |
| `session` | 세션 관리 |
| `navigation` | 페이지 이동 |
| `content` | 콘텐츠/텍스트 확인 |

### data_key 규칙
- [`config/test_data.json`](../config/test_data.json)의 키와 1:1 매핑
- Steps에서 `test_data[{data_key}].{속성}` 형식으로 참조
- 입력값이 필요 없는 케이스는 `null`

---

## 우선순위 (Priority)

| 등급 | 기준 |
|------|------|
| **high** | 핵심 기능 — 서비스 접근, 로그인, 주요 플로우 |
| **medium** | 보조 기능 — 유효성 검증, 에러 처리 |
| **low** | 엣지케이스 — 특수문자, 경계값, 대소문자 등 |

---

## 언어 규칙

- **기본 언어**: 한글
- **영어 사용**: UI 요소명, 버튼명, 입력값, 기술 용어
  - O: `Login 버튼 클릭`, `username 필드에 tomsmith 입력`
  - X: `로그인 버튼 클릭`, `사용자이름 필드에 tomsmith 입력`
- **화면 표시 텍스트 번역 금지**: 실제 UI에 보이는 문자 그대로 사용
  - O: `You logged into a secure area!`, `Your password is invalid!`
  - X: `로그인 성공 메시지`, `비밀번호가 틀립니다`

---

## 필수 필드 (4개)

| 필드 | 필수 | 설명 |
|------|------|------|
| 제목 (`#`) | **필수** | TC Summary — 테스트 목적 한줄 요약 |
| `## Precondition` | **필수** | 테스트 시작 전 시스템 상태 |
| `## Steps` | **필수** | 실행 단계 목록 (순서대로) |
| `## Expected` | **필수** | 기대 결과 |

---

## 필드별 작성 규칙

### 제목 (`#`)

- 무엇을 검증하는지 한눈에 파악 가능해야 함
- 15자 이내 간결하게

```markdown
# 정상 로그인 성공          ← Good
# 잘못된 비밀번호 오류 확인  ← Good
# 앱을 처음 설치했을 때 정상적으로 동작하는지 확인하는 테스트  ← Bad (너무 김)
```

---

### Precondition

- `0.` 으로 시작 (Step과 구분)
- 테스트 시작 직전 시스템 상태를 간결하게 명시

```markdown
## Precondition
0. 로그인 페이지 접속 상태       ← Good
0. 앱 미설치 상태                ← Good

## Precondition
앱이 설치되어 있어야 함          ← Bad (0. 형식 미준수)
```

---

### Steps

- `1.`, `2.`, `3.` 번호로 순서 명시
- 각 step = **단일 액션** (입력 or 클릭 or 이동 하나씩)
- 입력값은 `test_data[{data_key}].{속성}` 형식으로 참조 (하드코딩 금지)

```markdown
## Steps
1. username 필드에 test_data[valid_user].username 입력    ← Good
2. password 필드에 test_data[valid_user].password 입력
3. Login 버튼 클릭

## Steps
1. username 필드에 tomsmith 입력   ← Bad (하드코딩)
2. 로그인 정보 입력 후 Login 클릭   ← Bad (복수 액션을 하나에 묶음)
```

---

### Expected

- `-` 항목으로 검증 포인트 명시
- 실제 화면에 표시되는 **구체적 텍스트, 상태, UI 요소** 기재

```markdown
## Expected
- You logged into a secure area! 메시지가 표시되어야 한다.   ← Good
- Your password is invalid! 오류 메시지가 표시되어야 한다.   ← Good

## Expected
- 정상 동작함    ← Bad (검증 기준 없음)
- 에러 없음      ← Bad (구체적 상태 없음)
```

---

## 실제 케이스 예시

```markdown
---
id: tc_01
data_key: valid_user
priority: high
tags: [positive, smoke]
type: structured
---
# 정상 로그인 성공

## Precondition
0. 로그인 페이지 접속 상태

## Steps
1. username 필드에 test_data[valid_user].username 입력
2. password 필드에 test_data[valid_user].password 입력
3. Login 버튼 클릭

## Expected
- You logged into a secure area! 플래시 메시지가 표시되어야 한다.
```

```markdown
---
id: tc_08
data_key: sql_injection
priority: medium
tags: [security, negative]
type: structured
---
# SQL Injection 시도 차단 확인

## Precondition
0. 로그인 페이지 접속 상태

## Steps
1. username 필드에 test_data[sql_injection].username 입력
2. password 필드에 test_data[sql_injection].password 입력
3. Login 버튼 클릭

## Expected
- 로그인이 실패하고 오류 메시지가 표시되어야 한다. (보안 우회 불가)
```

---

## Quality Checklist

케이스 작성 완료 전 확인사항:

- [ ] 파일명이 `tc_{번호}_{설명}.md` 형식으로 작성됨
- [ ] **YAML frontmatter**가 파일 최상단에 있음 (`---` 블록)
- [ ] frontmatter 필수 필드 5개: `id`, `data_key`, `priority`, `tags`, `type`
- [ ] **priority**가 `high` / `medium` / `low` 중 하나
- [ ] **data_key**가 [`config/test_data.json`](../config/test_data.json) 키와 일치 (또는 `null`)
- [ ] Steps 입력값이 `test_data[{data_key}].{속성}` 형식 (하드코딩 금지)
- [ ] 제목이 테스트 목적을 명확하게 표현함 (15자 이내)
- [ ] `Precondition`이 `0.` 으로 시작함
- [ ] `Steps`가 `1.`, `2.` 번호 순서대로, 단일 액션씩 작성됨
- [ ] `Expected`가 `-` 항목으로 구체적 텍스트/상태를 명시함 ("정상 동작" 금지)
- [ ] 화면 UI 텍스트가 영어 원문 그대로 사용됨
- [ ] 하나의 파일에 하나의 케이스만 있음
