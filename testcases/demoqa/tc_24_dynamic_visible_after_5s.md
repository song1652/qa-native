---
id: tc_24
priority: medium
tags: [positive, elements, dynamic]
type: structured
---
# Button Becomes Visible After 5 Seconds

## Precondition
- https://demoqa.com 접속 상태

## Steps
1. https://demoqa.com/dynamic-properties 접속
2. "Visible After 5 Seconds" 버튼이 초기에 표시되지 않음을 확인
3. 5초 이상 대기

## Expected
- 5초 후 "Visible After 5 Seconds" 버튼이 페이지에 visible 상태로 나타남
- 버튼이 DOM에 추가되거나 hidden 속성이 해제됨
