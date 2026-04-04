# state/pipeline.json 구조

```json
{
  "url": "",
  "test_cases": [],
  "step": "init | analyzed | planned | generated | reviewed | approved | done | heal_needed | heal_failed",
  "dom_info": {},
  "dom_cache_key": "state/dom_cache/{url_md5_hash}.json",
  "plan": [],
  "cases_path": "testcases/{group}/",
  "group_dir": "{group}",
  "generated_file_path": "tests/generated/{group}/",
  "generated_files": [],
  "lint_result": {},
  "review_summary": "",
  "approval_status": "approved | rejected",
  "rejection_reason": "",
  "rejection_count": 0,
  "execution_result": {},
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
