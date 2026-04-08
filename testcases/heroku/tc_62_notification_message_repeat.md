---
id: tc_62_notification_message_repeat
data_key: null
priority: low
tags: [positive, interaction, notification]
type: structured
---
# 알림 메시지 반복 클릭 시 변경 확인

## Precondition
- https://the-internet.herokuapp.com/notification_message 접속 상태

## Steps
1. "Click here" 링크 클릭
2. 첫 번째 알림 메시지 텍스트 읽기
3. "Click here" 링크 다시 클릭
4. 두 번째 알림 메시지 텍스트 읽기

## Expected
- 클릭할 때마다 알림 메시지가 새로 표시된다
- 메시지가 "Action successful" 또는 "Action unsuccesful" 중 하나이다
