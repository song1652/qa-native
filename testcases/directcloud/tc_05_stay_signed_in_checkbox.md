---
id: tc_05_stay_signed_in_checkbox
data_key: null
priority: low
tags: [positive, auth, ui]
type: structured
---
# Stay signed in 체크박스 토글

## Precondition
- https://web.directcloud.jp/login 접속 상태

## Steps
1. 체크박스(input[type="checkbox"]) 가시성 확인 — 기본값은 체크됨
2. 체크박스 클릭 (해제)
3. 체크 해제 상태 확인
4. 체크박스 다시 클릭 (재체크)
5. 원래 체크 상태 복원 확인

## Expected
- 체크박스가 클릭마다 상태가 전환된다 (checked ↔ unchecked)
- 두 번 클릭 후 원래 상태로 복원된다
