---
id: tc_105
priority: medium
tags: [negative, elements, webtable]
type: structured
---
# Web Table Add Empty Submit Validation

## Precondition
- https://demoqa.com 접속 상태

## Steps
1. https://demoqa.com/webtables 페이지로 이동
2. "Add" 버튼 클릭
3. 등록 폼이 열린 상태에서 아무것도 입력하지 않고 "Submit" 버튼 클릭

## Expected
- 필수 필드(First Name, Last Name, Email, Age, Salary, Department)에 validation 에러(빨간 테두리 등) 표시
- 폼이 닫히지 않고 유지됨
