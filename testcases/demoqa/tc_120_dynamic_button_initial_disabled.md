---
id: tc_120
priority: medium
tags: [positive, elements, dynamic]
type: structured
---
# Dynamic Properties Button Initially Disabled

## Precondition
- https://demoqa.com 접속 상태

## Steps
1. https://demoqa.com/dynamic-properties 페이지로 이동
2. 페이지 로드 직후 "Will enable 5 seconds" 버튼 상태 즉시 확인 (5초 대기 없이)

## Expected
- "Will enable 5 seconds" 버튼이 disabled 상태임
- 버튼이 클릭 불가 상태로 표시됨
