---
id: tc_12_dynamic_controls_add_remove
data_key: null
priority: medium
tags: [positive, content]
type: structured
---
# Dynamic Controls 체크박스 제거/추가

## Precondition
- https://the-internet.herokuapp.com/dynamic_controls 접속 상태

## Steps
1. "Remove" 버튼 클릭
2. 로딩 완료 대기
3. 체크박스가 사라졌는지 확인
4. "Add" 버튼 클릭
5. 로딩 완료 대기

## Expected
- Remove 후 체크박스가 사라지고 "It's gone!" 메시지가 표시된다
- Add 후 체크박스가 다시 나타나고 "It's back!" 메시지가 표시된다
