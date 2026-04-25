---
id: tc_08_hover_user_info
data_key: null
priority: low
tags: [positive, hover, interaction]
type: structured
---
# Hover 시 사용자 정보 표시

## Precondition
- https://the-internet.herokuapp.com/hovers 접속 상태

## Steps
1. 첫 번째 사용자 이미지(.figure:nth-child(1) img)에 마우스를 올린다 (hover)
2. 표시된 캡션 텍스트를 확인한다
3. 두 번째 사용자 이미지(.figure:nth-child(2) img)에 마우스를 올린다
4. 표시된 캡션 텍스트를 확인한다

## Expected
- 첫 번째 이미지 hover 시 "name: user1" 텍스트가 포함된 캡션(.figcaption)이 표시된다
- 두 번째 이미지 hover 시 "name: user2" 텍스트가 포함된 캡션(.figcaption)이 표시된다
- 각 캡션에 "View profile" 링크가 포함된다
