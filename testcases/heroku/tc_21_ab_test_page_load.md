---
id: tc_21_ab_test_page_load
data_key: null
priority: medium
tags: [positive, content, abtest]
type: structured
---
# A/B 테스트 페이지 로드 확인

## Precondition
- https://the-internet.herokuapp.com/abtest 접속 상태

## Steps
1. 페이지 제목 요소 확인
2. 본문 텍스트 존재 확인

## Expected
- 페이지 제목이 "A/B Test Control" 또는 "A/B Test Variation 1"이다
- 본문 설명 텍스트가 표시된다
