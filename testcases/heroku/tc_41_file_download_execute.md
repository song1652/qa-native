---
id: tc_41_file_download_execute
data_key: null
priority: medium
tags: [positive, interaction, download]
type: structured
---
# 파일 다운로드 실행

## Precondition
- https://the-internet.herokuapp.com/download 접속 상태

## Steps
1. 첫 번째 다운로드 링크 클릭
2. 다운로드 이벤트 대기

## Expected
- 파일 다운로드가 시작된다
- 다운로드된 파일명이 링크 텍스트와 일치한다
