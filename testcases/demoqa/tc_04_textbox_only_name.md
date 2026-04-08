---
id: tc_04
priority: low
tags: [positive, elements, textbox]
type: structured
---
# Submit Text Box With Only Full Name

## Precondition
- https://demoqa.com 접속 상태

## Steps
1. https://demoqa.com/text-box 접속
2. Full Name 필드에 "Jane Smith" 입력
3. Email, Current Address, Permanent Address 필드는 비워둠
4. Submit 버튼 클릭

## Expected
- 하단 출력 영역(#output)이 표시됨
- Name: Jane Smith 텍스트가 출력 영역에 표시됨
- Email, Current Address, Permanent Address 항목은 출력 영역에 표시되지 않음
