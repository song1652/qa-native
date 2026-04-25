---
id: tc_10_logout
data_key: valid_user
priority: high
tags: [positive, smoke, auth]
type: structured
---
# 로그인 후 로그아웃

## Precondition
- https://the-internet.herokuapp.com/login 접속 상태

## Steps
1. Username 필드(#username)에 test_data[heroku][valid_user].username 입력
2. Password 필드(#password)에 test_data[heroku][valid_user].password 입력
3. Login 버튼(button[type="submit"]) 클릭
4. /secure 페이지로 이동 확인 후 Logout 버튼(a[href="/logout"]) 클릭

## Expected
- 로그아웃 후 /login 페이지로 리다이렉트된다
- "You logged out of the secure area!" 메시지(#flash)가 표시된다
- Logout 버튼이 더 이상 표시되지 않는다
