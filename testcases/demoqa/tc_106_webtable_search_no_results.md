---
id: tc_106
priority: medium
tags: [negative, elements, webtable]
type: structured
---
# Web Table Search No Results

## Precondition
- https://demoqa.com 접속 상태

## Steps
1. https://demoqa.com/webtables 페이지로 이동
2. 상단 검색창에 "zzzznonexistent" 입력

## Expected
- 테이블에 일치하는 행이 없음
- 빈 테이블(No rows found 또는 행 0개) 표시
