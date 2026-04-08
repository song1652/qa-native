---
id: tc_37
priority: medium
tags: [negative, forms, practice]
type: structured
---
# Form Invalid Email Validation

## Precondition
- https://demoqa.com 접속 상태

## Steps
1. https://demoqa.com/automation-practice-form 접속
2. First Name 필드에 "John" 입력
3. Last Name 필드에 "Doe" 입력
4. Email 필드에 "invalid" 입력 (유효하지 않은 형식)
5. Gender "Male" 라디오 버튼 선택
6. Mobile 필드에 "1234567890" 입력
7. Submit 버튼 클릭

## Expected
- 폼이 제출되지 않음
- Email 필드에 빨간 테두리(validation 에러)가 표시됨
- 제출 모달이 나타나지 않음
