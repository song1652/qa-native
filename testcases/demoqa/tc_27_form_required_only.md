---
id: tc_27
priority: high
tags: [positive, forms, practice]
type: structured
---
# Form Required Fields Only

## Precondition
- https://demoqa.com 접속 상태

## Steps
1. https://demoqa.com/automation-practice-form 접속
2. First Name 필드에 "Jane" 입력
3. Last Name 필드에 "Smith" 입력
4. Gender "Female" 라디오 버튼 선택
5. Mobile 필드에 "9876543210" 입력
6. Submit 버튼 클릭

## Expected
- 제출 완료 모달(Thanks for submitting the form)이 표시됨
- 선택 사항 필드 없이도 폼 제출이 성공함
