---
id: tc_25_normal_image_load
data_key: null
priority: low
tags: [positive, content, broken_images]
type: structured
---
# 정상 이미지 로드 확인

## Precondition
- https://the-internet.herokuapp.com/broken_images 접속 상태

## Steps
1. 페이지 내 모든 img 요소 수집
2. naturalWidth가 0보다 큰 이미지 확인

## Expected
- 정상적으로 로드된 이미지가 최소 1개 존재한다
