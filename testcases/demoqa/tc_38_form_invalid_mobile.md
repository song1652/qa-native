---
id: tc_38
priority: medium
tags: [negative, forms, practice]
type: structured
---
# Form Invalid Mobile Validation

## Precondition
- https://demoqa.com 접속 상태

## Steps
1. https://demoqa.com/automation-practice-form 접속
2. First Name 필드에 "John" 입력
3. Last Name 필드에 "Doe" 입력
4. Gender "Male" 라디오 버튼 선택
5. Mobile 필드에 "abc" 입력 (숫자가 아닌 값)
6. Submit 버튼 클릭

## Expected
- 폼이 제출되지 않음
- Mobile 필드에 빨간 테두리(validation 에러)가 표시됨
- 제출 모달이 나타나지 않음
