---
id: tc_04_login_wrong_company_code
data_key: wrong_company
priority: medium
tags: [negative, auth]
type: structured
---
# 존재하지 않는 회사코드로 로그인 실패

## Precondition
- https://web.directcloud.jp/login 접속 상태

## Steps
1. Company ID 필드([name="company_code"])에 test_data[directcloud][wrong_company].company 입력
2. User ID 필드([name="id"])에 test_data[directcloud][valid_user].username 입력
3. Password 필드([name="password"])에 test_data[directcloud][valid_user].password 입력
4. Login 버튼(#new_btn_login) 클릭

## Expected
- URL이 https://web.directcloud.jp/login 에 그대로 유지된다
- 로그인에 실패한다 (mybox 페이지로 이동하지 않는다)
