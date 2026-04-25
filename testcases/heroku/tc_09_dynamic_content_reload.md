---
id: tc_09_dynamic_content_reload
data_key: null
priority: low
tags: [positive, dynamic, content]
type: structured
---
# 동적 콘텐츠 페이지 새로고침 시 변경 확인

## Precondition
- https://the-internet.herokuapp.com/dynamic_content 접속 상태

## Steps
1. 페이지의 콘텐츠 행(.row .large-10)의 첫 번째 텍스트를 기록한다
2. 브라우저 새로고침(F5)을 수행한다
3. 새로고침 후 콘텐츠 행의 첫 번째 텍스트를 다시 읽는다

## Expected
- 페이지가 정상적으로 로드된다
- 콘텐츠 행(.row)이 3개 존재한다
- 각 행에 이미지(.large-2 img)와 텍스트(.large-10)가 포함된다
