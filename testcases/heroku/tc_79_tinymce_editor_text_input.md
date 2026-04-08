---
id: tc_79_tinymce_editor_text_input
data_key: null
priority: medium
tags: [positive, interaction, tinymce]
type: structured
---
# TinyMCE 에디터 텍스트 입력

## Precondition
- https://the-internet.herokuapp.com/tinymce 접속 상태

## Steps
1. TinyMCE 에디터 iframe으로 전환
2. 에디터 본문 영역 클릭
3. 기존 텍스트 전체 선택 후 삭제
4. "Hello Playwright" 텍스트 입력

## Expected
- 에디터에 "Hello Playwright" 텍스트가 입력된다
