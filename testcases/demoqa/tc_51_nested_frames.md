---
id: tc_51
priority: medium
tags: [positive, alerts, frames]
type: structured
---
# Nested Frames Show Parent and Child Text

## Precondition
- https://demoqa.com 접속 상태

## Steps
1. https://demoqa.com/nestedframes 접속
2. 부모 iframe으로 전환
3. 부모 iframe 내 텍스트 확인
4. 부모 iframe 내 자식 iframe으로 전환
5. 자식 iframe 내 텍스트 확인

## Expected
- 부모 iframe에 "Parent frame" 텍스트가 표시됨
- 자식 iframe에 "Child Iframe" 텍스트가 표시됨
