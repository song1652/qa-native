---
id: tc_51_infinite_scroll_load_more
data_key: null
priority: medium
tags: [positive, interaction, infinite_scroll]
type: structured
---
# 무한 스크롤 추가 콘텐츠 로드

## Precondition
- https://the-internet.herokuapp.com/infinite_scroll 접속 상태

## Steps
1. 초기 콘텐츠 블록 수 확인
2. 페이지 하단으로 스크롤
3. 새로운 콘텐츠 블록 로드 대기
4. 콘텐츠 블록 수 다시 확인

## Expected
- 스크롤 후 콘텐츠 블록 수가 증가한다
