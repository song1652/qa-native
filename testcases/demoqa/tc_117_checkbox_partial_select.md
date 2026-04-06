---
id: tc_117
priority: medium
tags: [positive, elements, checkbox]
type: structured
---
# Checkbox Partial Select Indeterminate State

## Precondition
- https://demoqa.com 접속 상태

## Steps
1. https://demoqa.com/checkbox 페이지로 이동
2. "Expand All" 버튼 클릭하여 전체 트리 펼치기
3. "Desktop" 하위의 "Notes" 체크박스만 클릭하여 체크

## Expected
- "Notes" 체크박스가 체크됨
- "Desktop" 노드가 반선택(indeterminate) 상태로 표시됨
- "Home" 노드도 반선택(indeterminate) 상태로 표시됨
