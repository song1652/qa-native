# state/pipeline.json 구조

```json
{
  "url": "",
  "test_cases": [],
  "step": "init | analyzed | planned | generated | reviewed | approved | done | heal_needed | heal_failed",
  "dom_info": {},
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
      { "test_id": "", "test_name": "", "traceback": "" }
    ],
    "raw_tail": "",
    "analyzed_at": ""
  }
}
```
