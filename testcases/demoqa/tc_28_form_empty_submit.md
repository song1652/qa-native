---
id: tc_28
priority: medium
tags: [negative, forms, practice]
type: structured
---
# Form Empty Submit Validation

## Precondition
- https://demoqa.com 접속 상태

## Steps
1. https://demoqa.com/automation-practice-form 접속
2. 아무 필드도 입력하지 않은 상태에서 Submit 버튼 클릭

## Expected
- 폼이 제출되지 않음
- 필수 필드(First Name, Last Name, Gender, Mobile)에 빨간 테두리(validation 에러)가 표시됨
- 제출 모달이 나타나지 않음
