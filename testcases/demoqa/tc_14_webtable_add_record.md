---
id: tc_14
priority: high
tags: [positive, elements, webtable]
type: structured
---
# Add New Record to Web Table

## Precondition
- https://demoqa.com 접속 상태

## Steps
1. https://demoqa.com/webtables 접속
2. "Add" 버튼 클릭
3. 등록 폼에서 First Name 필드에 "Alice" 입력
4. Last Name 필드에 "Brown" 입력
5. Email 필드에 "alice.brown@example.com" 입력
6. Age 필드에 "30" 입력
7. Salary 필드에 "50000" 입력
8. Department 필드에 "QA" 입력
9. Submit 버튼 클릭

## Expected
- 모달이 닫힘
- 테이블에 새로운 행이 추가됨
- 추가된 행에 "Alice", "Brown", "alice.brown@example.com", "30", "50000", "QA" 값이 표시됨
