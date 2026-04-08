---
id: tc_82_login_username_only
data_key: valid_user
priority: medium
tags: [negative, auth, login]
type: structured
---
# Username만 입력 후 로그인 시도

## Precondition
- https://the-internet.herokuapp.com/login 접속 상태

## Steps
1. Username 필드에 test_data[valid_user].username 입력
2. Password 필드는 비워둠
3. Login 버튼 클릭

## Expected
- "Your password is invalid!" 오류 메시지가 표시된다
