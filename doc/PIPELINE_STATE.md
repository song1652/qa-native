# state/pipeline.json 구조

```json
{
  "url": "",
  "test_cases": [],
  "step": "init | analyzed | planned | generated | reviewed (03_lint 완료) | done | heal_needed | heal_failed",
  "dom_info": {
    "title": "",
    "url": "",
    "inputs": [],
    "buttons": [],
    "errors": [],
    "links": [],
    "forms_count": 0,
    "components": [],
    "idElements": []
  },
  "sub_dom_keys": {
    "{sub_url}": "{url_md5_hash}"
  },
  "dom_cache_key": "state/dom_cache/{url_md5_hash}.json",
  "plan": [],
  "cases_path": "testcases/{group}/",
  "group_dir": "{group}",
  "generated_file_path": "tests/generated/{group}/",
  "generated_files": [],
  "lint_result": {},
  "review_summary": "",
  "approval_status": "(미사용 — 승인 단계 제거됨)",
  "rejection_reason": "(미사용)",
  "rejection_count": 0,
  "execution_result": {
    "passed": 0,
    "failed": 0,
    "total": 0,
    "pass_rate": 0.0,
    "exit_code": 0,
    "heal_count": 0,
    "json_report_path": "/tmp/qa_single_report_{ts}.json"
  },
  "heal_count": 0,
  "heal_context": {
    "heal_count": 0,
    "failure_count": 0,
    "failures": [
      { "test_id": "", "test_name": "", "traceback": "", "screenshot": null }
    ],
    "raw_tail": "",
    "analyzed_at": ""
  }
}
```

## state/heal_stats.json 구조

```json
{
  "version": 1,
  "description": "힐링 오류 패턴별 빈도 카운터",
  "patterns": {
    "{error_type}::{summary}": {
      "count": 1,
      "error_type": "Locator | Assertion | Timeout | URL | 기타",
      "summary": "핵심 오류 라인 (최대 120자)",
      "first_seen": "ISO datetime",
      "last_seen": "ISO datetime"
    }
  }
}
```

## state/run_history.json 구조

매 실행(단일/병렬) 완료 시 `append_run_history()`가 자동으로 한 줄씩 추가하는 배열.

```json
[
  {
    "timestamp": "YYYY-MM-DD HH:MM:SS",
    "pipeline": "single | parallel",
    "group": "{group_name}",
    "groups": ["{group_a}", "{group_b}"],
    "passed": 10,
    "failed": 0,
    "total": 10,
    "pass_rate": 100.0,
    "heal_count": 0,
    "first_pass": true,
    "duration_sec": 12.3
  }
]
```

| 필드 | 설명 |
|------|------|
| `pipeline` | `single` (05_execute.py) 또는 `parallel` (99_merge.py) |
| `group` | 단일 파이프라인: 대상 그룹명 |
| `groups` | 병렬 파이프라인: 실행된 그룹 목록 |
| `first_pass` | 힐링 없이 첫 실행 통과 여부 (생성 코드 품질 프록시) |
| `duration_sec` | pytest 포함 전체 소요 시간 (초) |

## dom_info 필드 상세

| 필드 | 설명 |
|------|------|
| `components[]` | React/UI 컴포넌트 목록: tabs, checkboxes, tree, draggable, react-select, accordion, progressbar, slider, modal 등. 각 항목은 `{ type, selector, text/label, ... }` |
| `idElements[]` | 페이지 내 모든 가시 요소의 ID 목록. 각 항목은 `{ id, tag, class }` |

## sub_dom_keys 필드

서브페이지 URL → 캐시 해시 매핑. `01_analyze.py`가 서브페이지를 분석한 뒤 `state/dom_cache/{hash}.json`에 저장하고, 경로 대신 해시만 pipeline.json에 기록한다.
실제 서브 DOM은 `_paths.resolve_sub_doms(state)`로 캐시 파일에서 로드한다. (pipeline.json에 인라인 저장하지 않음)

## execution_result 필드 상세

| 필드 | 설명 |
|------|------|
| `passed` | 통과 테스트 수 |
| `failed` | 실패 테스트 수 |
| `total` | 전체 테스트 수 |
| `pass_rate` | 통과율 (%) |
| `exit_code` | pytest 종료코드 (0=성공, 1=실패) |
| `heal_count` | 이 execution에서 적용된 힐링 횟수 |
| `json_report_path` | pytest-json-report 파일 경로 (06_heal.py가 재활용, 삭제하지 않음) |

## 힐링 프로세스

- `heal_count` (top-level): 단계별 누적 힐링 횟수. 최대 3회 제한.
- `execution_result.heal_count`: 마지막 실행 시점의 힐링 횟수.
- 초과 시 `step = "heal_failed"`, 종료코드 2로 파이프라인 중단.
