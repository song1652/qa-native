---
id: tc_22_ab_test_content_variation
data_key: null
priority: low
tags: [positive, content, abtest]
type: structured
---
# A/B 테스트 콘텐츠 변형 확인

## Precondition
- https://the-internet.herokuapp.com/abtest 접속 상태

## Steps
1. 페이지 제목 텍스트 읽기
2. 페이지 새로고침 후 제목 텍스트 다시 읽기

## Expected
- 제목이 "A/B Test Control" 또는 "A/B Test Variation 1" 중 하나이다
- 콘텐츠 영역(div.example)이 존재한다
