---
id: tc_18
priority: low
tags: [positive, elements, webtable]
type: structured
---
# Web Table Pagination and Rows Per Page

## Precondition
- https://demoqa.com 접속 상태

## Steps
1. https://demoqa.com/webtables 접속
2. rows per page 드롭다운을 찾아 "5" 옵션 선택
3. 현재 표시되는 행 수 확인
4. rows per page 드롭다운을 "10"으로 변경
5. 현재 표시되는 행 수 확인

## Expected
- rows per page "5" 선택 시 최대 5행이 테이블에 표시됨
- rows per page "10" 선택 시 최대 10행이 테이블에 표시됨
- 드롭다운 값 변경이 테이블에 즉시 반영됨
