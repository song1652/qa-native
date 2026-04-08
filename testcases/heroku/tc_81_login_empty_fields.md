---
id: tc_81_login_empty_fields
data_key: null
priority: medium
tags: [negative, auth, login]
type: structured
---
# 로그인 빈 필드 제출

## Precondition
- https://the-internet.herokuapp.com/login 접속 상태

## Steps
1. Username과 Password 필드를 비워둔 상태로 Login 버튼 클릭

## Expected
- "Your username is invalid!" 오류 메시지가 표시된다
