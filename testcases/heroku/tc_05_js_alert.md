---
id: tc_05_js_alert
data_key: null
priority: medium
tags: [positive, javascript, dialog]
type: structured
---
# JavaScript Alert 확인

## Precondition
- https://the-internet.herokuapp.com/javascript_alerts 접속 상태

## Steps
1. "Click for JS Alert" 버튼(button:has-text("Click for JS Alert"))을 클릭한다
2. 팝업 Alert 대화상자를 수락(accept)한다

## Expected
- Alert 대화상자가 "I am a JS Alert" 텍스트를 포함한다
- 수락 후 결과 메시지(#result)가 "You successfully clicked an alert" 텍스트를 표시한다
