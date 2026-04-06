---
id: tc_23
priority: medium
tags: [positive, elements, dynamic]
type: structured
---
# Button Color Changes After 5 Seconds

## Precondition
- https://demoqa.com 접속 상태

## Steps
1. https://demoqa.com/dynamic-properties 접속
2. "Color Change" 버튼의 초기 CSS class 확인
3. 5초 이상 대기

## Expected
- 5초 후 "Color Change" 버튼의 CSS class가 변경됨 (예: text-danger 클래스 추가)
- 버튼의 색상이 시각적으로 변경됨
