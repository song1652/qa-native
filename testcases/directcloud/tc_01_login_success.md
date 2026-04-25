---
id: tc_01_login_success
data_key: valid_user
priority: high
tags: [positive, smoke, auth]
type: structured
---
# 정상 로그인 성공

## Precondition
- https://web.directcloud.jp/login 접속 상태

## Steps
1. Company ID 필드([name="company_code"])에 test_data[directcloud][valid_user].company 입력
2. User ID 필드([name="id"])에 test_data[directcloud][valid_user].username 입력
3. Password 필드([name="password"])에 test_data[directcloud][valid_user].password 입력
4. Login 버튼(#new_btn_login) 클릭

## Expected
- URL이 https://web.directcloud.jp/mybox/ 형태로 변경된다
- 검색창(#inputSearch)이 표시된다
- 메인 파일 목록 영역(#main)이 표시된다
