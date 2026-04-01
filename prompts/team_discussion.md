# 팀 토론 심의 프롬프트 (team_discuss.py 후 사용)

아래 주제로 사수/부사수가 최소 3회 왕복(6발언) 실제 대화를 나눈 후 결론을 도출하라.

topic: {ctx.topic}
rejection_reason: {ctx.rejection_reason}  (재토론이면 반드시 반영)
team_charter: {ctx.team_charter}
team_notes: {ctx.team_notes}  (기존 결정 — 중복 지양)
lessons_learned: {ctx.lessons_learned}

## 진행 방식

라운드마다 아래 순서를 반복한다. **각 발언 후 즉시 dialog.json에 append 저장.**

[라운드 1]
사수 발언 -> dialog.json 저장 (messages에 append)
부사수 반응 -> dialog.json 저장

[라운드 2]
사수 반론·보완 -> dialog.json 저장
부사수 동의·추가 의견 -> dialog.json 저장

[라운드 3]
사수 쟁점 정리·방향 제시 -> dialog.json 저장
부사수 최종 의견·예시 보완 -> dialog.json 저장

(필요 시 라운드 추가 — 주제가 복잡하거나 이견이 있으면 4~5라운드까지)

[결론]
from: "deliberation" 메시지로 합의 사항 정리 -> dialog.json 저장
session.status = "discussed", session.completed_at = 현재시각

## 역할 지침

사수:
- 첫 발언: 문제·위험 요소 분석, 방향 제시
- 이후 발언: 부사수 의견에 반응하며 보완하거나 반론
- 단답 금지 — 구체적 근거와 예외 케이스 포함

부사수:
- 사수 발언에 직접 반응 (동의·보완·질문·**반론** 중 택1)
- "실제 적용 시 어려운 점"과 구체적 예시 제시
- **무조건 동의 금지** — 매 라운드 최소 1가지는 다른 시각·우려·대안을 제시할 것
- 사수의 결론이 맞더라도 "다른 방법은 없는지", "빠진 관점은 없는지" 반드시 점검
- "동의합니다" 단독 발언 금지 — 동의하더라도 구체적 보충·예외 사례·실행 시 어려움을 함께 언급

## 저장 형식 (발언마다 즉시)

dialog.json의 마지막 session.messages에 아래 형식으로 append:
```json
{
  "from": "senior" | "junior" | "deliberation",
  "timestamp": "현재시각 ISO",
  "content": "발언 내용"
}
```
deliberation 메시지에는 "status": "discussed" 추가.

## 저장 방식 강제 규칙
- 반드시 Edit tool로 messages 배열 마지막에 항목 1개씩 append
- Write tool로 전체 파일 덮어쓰기 금지 (배치 저장 금지)
- 발언 작성 -> Edit 저장 -> 다음 발언 작성 -> Edit 저장 순서 엄수
