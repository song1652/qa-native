---
id: tc_05
priority: low
tags: [positive, elements, textbox]
type: structured
---
# Submit Text Box With Long Current Address

## Precondition
- https://demoqa.com 접속 상태

## Steps
1. https://demoqa.com/text-box 접속
2. Current Address 필드에 300자 이상의 긴 텍스트 입력 (예: "A" * 300 또는 임의의 긴 문자열)
3. Submit 버튼 클릭

## Expected
- 하단 출력 영역(#output)이 표시됨
- Current Address 항목에 입력한 전체 텍스트가 잘리지 않고 출력 영역에 표시됨
