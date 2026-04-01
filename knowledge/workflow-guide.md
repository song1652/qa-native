# QA-Native 워크플로우 빠른 참조

> 실행 명령어·힐링 기준·토론 절차 상세는 [`CLAUDE.md`](../CLAUDE.md) 참조.
> 단계별 역할 정의 상세는 [`agents/team_charter.md`](../agents/team_charter.md) 참조.

---

## 단일 vs 병렬 비교

| | 단일 (`run_qa.py`) | 병렬 (`run_qa_parallel.py`) |
|---|---|---|
| 심의 | 단계별 Agent 호출 | subagent가 심의 없이 직접 코드 생성 |
| 코드 위치 | `tests/generated/test_generated.py` | `tests/generated/{그룹}/{label}.py` |
| 실행 | pytest 단일 파일 | pytest 다중 파일 (parallel workers) |
| 리포트 | `report_{ts}.html` | `parallel_index_{ts}.html` |
| 힐링 | `06_heal.py` → `06a_dialog.py` → Agent | `99_merge.py` → `state/heal_context.json` → Claude |
