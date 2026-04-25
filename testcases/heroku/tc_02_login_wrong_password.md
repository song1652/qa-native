---
id: tc_02_login_wrong_password
data_key: invalid_user
priority: high
tags: [negative, auth]
type: structured
---
# 잘못된 비밀번호로 로그인 실패

## Precondition
- https://the-internet.herokuapp.com/login 접속 상태

## Steps
1. Username 필드(#username)에 test_data[heroku][invalid_user].username 입력
2. Password 필드(#password)에 test_data[heroku][invalid_user].password 입력
3. Login 버튼(button[type="submit"]) 클릭

## Expected
- URL이 /login으로 유지된다
- 에러 메시지(#flash.error)가 표시된다
- 에러 메시지에 "Your username is invalid!" 또는 "Your password is invalid!" 텍스트가 포함된다
