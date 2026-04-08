---
id: tc_81
priority: medium
tags: [positive, interactions, resizable]
type: structured
---
# Resizable Box With Constraint

## Precondition
- https://demoqa.com 접속 상태

## Steps
1. https://demoqa.com/resizable 페이지로 이동
2. "Resizable box with restriction" 박스 확인 (최소 150x150, 최대 500x300)
3. 박스 우측 하단 리사이즈 핸들을 드래그하여 크기 변경 시도

## Expected
- 박스 크기가 변경되되, 제한 범위(최소 150x150, 최대 500x300) 내에서만 변경됨
