---
id: tc_110
priority: medium
tags: [positive, interactions, selectable]
type: structured
---
# Selectable Deselect Item

## Precondition
- https://demoqa.com 접속 상태

## Steps
1. https://demoqa.com/selectable 페이지로 이동
2. "List" 탭이 활성화된 상태 확인
3. 리스트에서 첫 번째 항목 클릭 (선택)
4. 같은 항목을 다시 클릭 (선택 해제)

## Expected
- 두 번째 클릭 후 해당 항목의 active 상태가 제거됨 (배경색 원래대로 복귀)
