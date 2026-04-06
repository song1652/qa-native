---
id: tc_50
priority: low
tags: [positive, alerts, frames]
type: structured
---
# Small Frame Contains Sample Page Text

## Precondition
- https://demoqa.com 접속 상태

## Steps
1. https://demoqa.com/frames 접속
2. 두 번째 작은 iframe으로 전환
3. iframe 내부 텍스트 확인

## Expected
- 두 번째 작은 iframe 안에 "This is a sample page" 텍스트가 visible 상태로 표시됨
