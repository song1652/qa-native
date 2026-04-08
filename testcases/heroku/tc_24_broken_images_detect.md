---
id: tc_24_broken_images_detect
data_key: null
priority: medium
tags: [positive, content, broken_images]
type: structured
---
# 깨진 이미지 감지

## Precondition
- https://the-internet.herokuapp.com/broken_images 접속 상태

## Steps
1. 페이지 내 모든 img 요소 수집
2. 각 이미지의 naturalWidth 속성 확인

## Expected
- 페이지에 이미지 요소가 3개 존재한다
- naturalWidth가 0인 깨진 이미지가 존재한다
