---
id: tc_55_javascript_error_console
data_key: null
priority: low
tags: [negative, error, javascript_error]
type: structured
---
# JavaScript 에러 페이지 콘솔 에러 확인

## Precondition
- https://the-internet.herokuapp.com/javascript_error 접속 상태

## Steps
1. 브라우저 콘솔 에러 리스너 등록
2. 페이지 로드 완료 대기
3. 콘솔 에러 메시지 수집

## Expected
- JavaScript 콘솔에 에러가 발생한다
- 에러 메시지에 "Cannot read properties of undefined" 텍스트가 포함된다
