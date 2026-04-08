---
id: tc_84_sql_injection_login
data_key: null
priority: low
tags: [negative, security, login]
type: structured
---
# SQL Injection 로그인 시도

## Precondition
- https://the-internet.herokuapp.com/login 접속 상태

## Steps
1. Username 필드에 "' OR '1'='1" 입력
2. Password 필드에 "' OR '1'='1" 입력
3. Login 버튼 클릭

## Expected
- 로그인이 실패한다
- "Your username is invalid!" 오류 메시지가 표시된다
