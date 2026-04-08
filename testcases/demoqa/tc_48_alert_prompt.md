---
id: tc_48
priority: high
tags: [positive, alerts]
type: structured
---
# Prompt Alert Accepts Input and Displays It

## Precondition
- https://demoqa.com 접속 상태

## Steps
1. https://demoqa.com/alerts 접속
2. prompt 버튼 클릭
3. 나타난 prompt 대화상자에 "TestUser" 입력
4. OK 선택

## Expected
- prompt 대화상자가 발생함
- OK 선택 후 페이지에 "You entered TestUser" 텍스트가 표시됨
