---
id: tc_01_login_success
data_key: valid_user
priority: high
tags: [positive, smoke, auth]
type: structured
---
# 정상 로그인 성공

## Precondition
- https://the-internet.herokuapp.com/login 접속 상태

## Steps
1. Username 필드(#username)에 test_data[heroku][valid_user].username 입력
2. Password 필드(#password)에 test_data[heroku][valid_user].password 입력
3. Login 버튼(button[type="submit"]) 클릭

## Expected
- URL이 /secure 로 변경된다
- "You logged into a secure area!" 성공 메시지(#flash)가 표시된다
- Logout 버튼(a[href="/logout"])이 표시된다
