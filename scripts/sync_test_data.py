"""
test_data.json 동기화 스크립트.
testcases/ 폴더의 tc_*.md frontmatter에서 data_key를 추출하고,
config/test_data.json에 누락된 키가 있으면 빈 템플릿을 자동 추가한다.

사용법: python scripts/sync_test_data.py [--dry-run]
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from parse_cases import load_cases


def main():
    dry_run = "--dry-run" in sys.argv

    project_root = Path(__file__).resolve().parent.parent
    testcases_dir = project_root / "testcases"
    test_data_path = project_root / "config" / "test_data.json"

    if not test_data_path.exists():
        print("[오류] config/test_data.json이 없습니다.")
        sys.exit(1)

    with open(test_data_path, encoding="utf-8") as f:
        test_data = json.load(f)

    added_count = 0

    for group_dir in sorted(testcases_dir.iterdir()):
        if not group_dir.is_dir() or group_dir.name.startswith("."):
            continue

        group = group_dir.name
        cases = load_cases(group_dir)

        if group not in test_data:
            test_data[group] = {}

        for case in cases:
            dk = case.get("data_key")
            if dk is None or dk in test_data[group]:
                continue

            # 빈 템플릿 추가
            test_data[group][dk] = {"username": "", "password": ""}
            added_count += 1
            print(f"  [추가] {group}/{dk}")

    if added_count == 0:
        print("[동기화] 누락된 data_key 없음. test_data.json이 최신입니다.")
        return

    if dry_run:
        print(f"\n[dry-run] {added_count}개 키 추가 예정 (실제 저장하지 않음)")
    else:
        with open(test_data_path, "w", encoding="utf-8") as f:
            json.dump(test_data, f, ensure_ascii=False, indent=2)
            f.write("\n")
        print(f"\n[완료] {added_count}개 키 추가됨 → {test_data_path}")


if __name__ == "__main__":
    main()
