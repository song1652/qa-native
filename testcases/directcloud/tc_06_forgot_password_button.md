---
id: tc_06_forgot_password_button
data_key: null
priority: medium
tags: [positive, auth, navigation]
type: structured
---
# Forgot Password 버튼 동작 확인

## Precondition
- https://web.directcloud.jp/login 접속 상태

## Steps
1. "Forgot Password?" 버튼(button:has-text("Forgot Password?")) 가시성 확인
2. "Forgot Password?" 버튼 클릭

## Expected
- 클릭 후 비밀번호 재설정 관련 화면 또는 모달이 표시된다
- 페이지가 정상적으로 반응한다 (오류 없음)
