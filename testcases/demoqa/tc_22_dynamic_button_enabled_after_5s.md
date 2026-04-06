---
id: tc_22
priority: medium
tags: [positive, elements, dynamic]
type: structured
---
# Button Becomes Enabled After 5 Seconds

## Precondition
- https://demoqa.com 접속 상태

## Steps
1. https://demoqa.com/dynamic-properties 접속
2. "Will enable 5 seconds" 버튼이 초기에 disabled 상태임을 확인
3. 5초 이상 대기

## Expected
- 5초 후 "Will enable 5 seconds" 버튼이 enabled 상태로 변경됨
- 버튼이 클릭 가능한 상태가 됨
