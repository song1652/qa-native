---
id: tc_71_slow_resources_load
data_key: null
priority: medium
tags: [positive, content, slow_resources]
type: structured
---
# 느린 리소스 로드 대기

## Precondition
- https://the-internet.herokuapp.com/slow 접속 상태

## Steps
1. 페이지 로드 완료 대기 (최대 30초)
2. 페이지 콘텐츠 확인

## Expected
- 느린 리소스 로드 후 페이지가 정상 표시된다
- "Slow Resources" 제목이 표시된다
