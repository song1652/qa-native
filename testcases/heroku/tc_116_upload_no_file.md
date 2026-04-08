---
id: tc_116_upload_no_file
data_key: null
priority: low
tags: [negative, interaction, upload]
type: structured
---
# 파일 선택 없이 업로드 시도

## Precondition
- https://the-internet.herokuapp.com/upload 접속 상태

## Steps
1. 파일을 선택하지 않은 상태에서 "Upload" 버튼 클릭

## Expected
- 오류 메시지가 표시되거나 업로드가 실패한다
- "Internal Server Error" 또는 에러 페이지가 표시된다
