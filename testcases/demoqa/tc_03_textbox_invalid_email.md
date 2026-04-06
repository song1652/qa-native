---
id: tc_03
priority: medium
tags: [negative, elements, textbox]
type: structured
---
# Submit Text Box With Invalid Email

## Precondition
- https://demoqa.com 접속 상태

## Steps
1. https://demoqa.com/text-box 접속
2. Email 필드에 "invalid-email" 입력
3. Submit 버튼 클릭

## Expected
- Email 필드에 에러 표시 (빨간 테두리 등 시각적 오류 표시)
- 출력 영역에 유효하지 않은 이메일이 표시되지 않거나, 에러 클래스가 적용됨
