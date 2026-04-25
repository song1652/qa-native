---
id: tc_03_checkboxes
data_key: null
priority: medium
tags: [positive, form, interaction]
type: structured
---
# 체크박스 선택/해제

## Precondition
- https://the-internet.herokuapp.com/checkboxes 접속 상태

## Steps
1. 페이지의 체크박스 목록(#checkboxes input[type="checkbox"])을 모두 가져온다
2. 첫 번째 체크박스(checkbox 1)를 클릭한다
3. 두 번째 체크박스(checkbox 2)를 클릭한다

## Expected
- 첫 번째 체크박스가 초기 상태(unchecked)에서 checked로 변경된다
- 두 번째 체크박스가 초기 상태(checked)에서 unchecked로 변경된다
