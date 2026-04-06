---
id: tc_104
priority: medium
tags: [negative, elements, links]
type: structured
---
# Links Not Found API Call

## Precondition
- https://demoqa.com 접속 상태

## Steps
1. https://demoqa.com/links 페이지로 이동
2. "Not Found" API call 링크 클릭
3. 하단 응답 메시지가 나타날 때까지 대기

## Expected
- 하단에 status 404와 "Not Found" 메시지 표시
