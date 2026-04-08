---
id: tc_93_remove_all_added_elements
data_key: null
priority: medium
tags: [positive, interaction, add_remove]
type: structured
---
# 추가된 요소 모두 삭제

## Precondition
- https://the-internet.herokuapp.com/add_remove_elements/ 접속 상태

## Steps
1. "Add Element" 버튼 3회 클릭
2. 생성된 "Delete" 버튼 3개 모두 클릭
3. "Delete" 버튼 존재 여부 확인

## Expected
- 모든 "Delete" 버튼이 삭제된다
- elements 영역이 비어있다
