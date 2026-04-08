---
id: tc_85_xss_script_login
data_key: null
priority: low
tags: [negative, security, login]
type: structured
---
# XSS 스크립트 로그인 시도

## Precondition
- https://the-internet.herokuapp.com/login 접속 상태

## Steps
1. Username 필드에 "<script>alert('xss')</script>" 입력
2. Password 필드에 "test" 입력
3. Login 버튼 클릭

## Expected
- 로그인이 실패한다
- Alert 다이얼로그가 발생하지 않는다
- "Your username is invalid!" 오류 메시지가 표시된다
