---
id: tc_03_login_empty_fields
data_key: null
priority: medium
tags: [negative, auth, validation]
type: structured
---
# 빈 필드로 로그인 시도

## Precondition
- https://web.directcloud.jp/login 접속 상태
- 모든 입력 필드가 비어 있는 상태

## Steps
1. 아무것도 입력하지 않고 Login 버튼(#new_btn_login) 클릭

## Expected
- URL이 https://web.directcloud.jp/login 에 그대로 유지된다
- Company ID 필드([name="company_code"])가 표시된다
- 로그인이 진행되지 않는다
