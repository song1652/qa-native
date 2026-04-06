---
id: tc_111
priority: medium
tags: [positive, interactions, droppable]
type: structured
---
# Droppable Prevent Propagation Not Greedy Inner Drop

## Precondition
- https://demoqa.com 접속 상태

## Steps
1. https://demoqa.com/droppable 페이지로 이동
2. "Prevent Propagation" 탭 클릭
3. "Drag me" 요소를 "Not Greedy" 영역의 내부 드롭존(Inner droppable (not greedy))으로 드래그 앤 드롭

## Expected
- 내부 드롭존에 "Dropped!" 텍스트 표시
- 외부 드롭존(Outer droppable)에도 "Dropped!" 텍스트 표시 (이벤트 버블링)
