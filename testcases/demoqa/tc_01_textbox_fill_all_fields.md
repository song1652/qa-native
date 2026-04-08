---
id: tc_01
priority: high
tags: [positive, elements, textbox]
type: structured
---
# Fill All Text Box Fields and Submit

## Precondition
- https://demoqa.com 접속 상태

## Steps
1. https://demoqa.com/text-box 접속
2. Full Name 필드에 "John Doe" 입력
3. Email 필드에 "john.doe@example.com" 입력
4. Current Address 필드에 "123 Main St, Springfield" 입력
5. Permanent Address 필드에 "456 Oak Ave, Shelbyville" 입력
6. Submit 버튼 클릭

## Expected
- 하단 출력 영역(#output)이 표시됨
- Name: John Doe 텍스트가 출력 영역에 표시됨
- Email: john.doe@example.com 텍스트가 출력 영역에 표시됨
- Current Address: 123 Main St, Springfield 텍스트가 출력 영역에 표시됨
- Permanent Address: 456 Oak Ave, Shelbyville 텍스트가 출력 영역에 표시됨
