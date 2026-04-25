---
id: tc_02_login_wrong_password
data_key: invalid_user
priority: high
tags: [negative, auth]
type: structured
---
# 잘못된 비밀번호로 로그인 실패

## Precondition
- https://web.directcloud.jp/login 접속 상태

## Steps
1. Company ID 필드([name="company_code"])에 test_data[directcloud][valid_user].company 입력
2. User ID 필드([name="id"])에 test_data[directcloud][valid_user].username 입력
3. Password 필드([name="password"])에 test_data[directcloud][invalid_user].password 입력
4. Login 버튼(#new_btn_login) 클릭

## Expected
- URL이 https://web.directcloud.jp/login 에 그대로 유지된다
- 로그인 폼이 여전히 표시된다 (로그인 페이지 유지)
