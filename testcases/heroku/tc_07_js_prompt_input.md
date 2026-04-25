---
id: tc_07_js_prompt_input
data_key: js_prompt
priority: medium
tags: [positive, javascript, dialog]
type: structured
---
# JavaScript Prompt 텍스트 입력

## Precondition
- https://the-internet.herokuapp.com/javascript_alerts 접속 상태

## Steps
1. "Click for JS Prompt" 버튼(button:has-text("Click for JS Prompt"))을 클릭한다
2. Prompt 대화상자에 test_data[heroku][js_prompt].text 를 입력한다
3. Prompt 대화상자를 수락(accept)한다

## Expected
- 결과 메시지(#result)가 "You entered: Hello Playwright" 텍스트를 표시한다
