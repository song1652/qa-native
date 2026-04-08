---
id: tc_25
priority: low
tags: [positive, elements, dynamic]
type: structured
---
# Button ID Changes on Each Page Load

## Precondition
- https://demoqa.com 접속 상태

## Steps
1. https://demoqa.com/dynamic-properties 접속
2. 랜덤 ID를 가진 버튼의 id 속성값 기록
3. 페이지 새로고침(reload)
4. 동일 버튼의 id 속성값 다시 확인

## Expected
- 새로고침 후 버튼의 id 값이 이전과 다른 값으로 변경됨
- 매 페이지 로드마다 id 값이 다르게 생성됨
