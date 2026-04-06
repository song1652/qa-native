---
id: tc_47
priority: medium
tags: [negative, alerts]
type: structured
---
# Confirm Alert Dismiss Shows Cancel Message

## Precondition
- https://demoqa.com 접속 상태

## Steps
1. https://demoqa.com/alerts 접속
2. "Do you confirm action?" confirm 버튼 클릭
3. 나타난 confirm 대화상자에서 Cancel 선택

## Expected
- confirm 대화상자가 발생함
- Cancel 선택 후 페이지에 "You selected Cancel" 텍스트가 표시됨
