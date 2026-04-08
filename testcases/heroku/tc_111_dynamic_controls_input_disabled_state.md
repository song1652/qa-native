---
id: tc_111_dynamic_controls_input_disabled_state
data_key: null
priority: low
tags: [negative, interaction, dynamic_controls]
type: structured
---
# Dynamic Controls 비활성화 상태에서 입력 시도

## Precondition
- https://the-internet.herokuapp.com/dynamic_controls 접속 상태

## Steps
1. 텍스트 입력 필드가 비활성화 상태인지 확인
2. 입력 필드에 텍스트 입력 시도

## Expected
- 입력 필드가 disabled 속성을 가진다
- 텍스트 입력이 불가능하다
