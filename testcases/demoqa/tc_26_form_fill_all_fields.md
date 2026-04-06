---
id: tc_26
priority: high
tags: [positive, forms, practice]
type: structured
---
# Form Fill All Fields

## Precondition
- https://demoqa.com 접속 상태

## Steps
1. https://demoqa.com/automation-practice-form 접속
2. First Name 필드에 "John" 입력
3. Last Name 필드에 "Doe" 입력
4. Email 필드에 "john@test.com" 입력
5. Gender "Male" 라디오 버튼 선택
6. Mobile 필드에 "1234567890" 입력
7. Date of Birth 필드 클릭 후 날짜 선택 (예: 01/01/1990)
8. Subjects 필드에 "Maths" 입력 후 자동완성에서 선택
9. Hobbies "Sports" 체크박스 선택
10. Upload Picture 버튼 클릭 후 임시 파일 업로드
11. Current Address 필드에 "123 Test Street" 입력
12. State 드롭다운에서 "NCR" 선택
13. City 드롭다운에서 "Delhi" 선택
14. Submit 버튼 클릭

## Expected
- 제출 완료 모달(Thanks for submitting the form)이 표시됨
- 모달 테이블에 입력한 값들(Student Name, Student Email, Gender, Mobile, Date of Birth, Subjects, Hobbies, Picture, Address, State and City)이 올바르게 표시됨
