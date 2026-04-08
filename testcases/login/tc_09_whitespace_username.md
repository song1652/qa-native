# 공백만 있는 username으로 로그인 시도

## Precondition
0. 로그인 페이지 접속 상태

## Steps
1. username 필드에 공백 문자(   ) 입력
2. password 필드에 SuperSecretPassword! 입력
3. Login 버튼 클릭

## Expected
- Your username is invalid! 오류 메시지가 표시되어야 한다.
- 로그인 페이지에 그대로 머물러야 한다.
