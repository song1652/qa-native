"""
테스트 케이스 파일 파서.

지원 형식:
  - *.md  : Markdown 구조화 형식 (# Title / ## Precondition / ## Steps / ## Expected)
  - *.json: JSON 배열 형식 (기존 호환)

반환값: normalize된 test_cases 리스트
"""
import json
import re
from pathlib import Path


def parse_md(text: str) -> list:
    """
    Markdown 파일을 test_cases 리스트로 파싱.

    형식:
        # 케이스 타이틀

        ## Precondition
        0. 사전 조건 내용

        ## Steps
        1. 첫 번째 스텝
        2. 두 번째 스텝

        ## Expected
        - 기대 결과

        ---   (케이스 구분자)
    """
    cases = []
    blocks = re.split(r"^\s*---+\s*$", text, flags=re.MULTILINE)

    for block in blocks:
        block = block.strip()
        if not block:
            continue

        title_match = re.search(r"^#\s+(.+)$", block, re.MULTILINE)
        title = title_match.group(1).strip() if title_match else "unnamed"

        precondition = _extract_section(block, "Precondition")
        steps_raw = _extract_section(block, "Steps")
        expected = _extract_section(block, "Expected")

        # Steps: 번호 있는 줄들을 리스트로
        steps = [
            line.strip()
            for line in steps_raw.splitlines()
            if re.match(r"^\d+\.", line.strip())
        ] if steps_raw else []

        cases.append({
            "title": title,
            "precondition": precondition.strip(),
            "steps": steps,
            "expected": expected.strip(),
            "format": "structured",
        })

    return cases


def _extract_section(text: str, section: str) -> str:
    """## Section 헤더 아래의 내용을 추출."""
    pattern = rf"##\s+{section}\s*\n(.*?)(?=\n##|\Z)"
    match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
    return match.group(1).strip() if match else ""


def parse_json(text: str) -> list:
    """JSON 배열을 test_cases 리스트로 파싱 (기존 형식 호환)."""
    raw = json.loads(text)
    normalized = []
    for item in raw:
        if isinstance(item, str):
            normalized.append({
                "title": item,
                "precondition": "",
                "steps": [],
                "expected": "",
                "format": "natural",
            })
        elif isinstance(item, dict):
            normalized.append({
                "title": item.get("title", "unnamed"),
                "precondition": item.get("precondition", ""),
                "steps": item.get("steps", []),
                "expected": item.get("expected", ""),
                "format": "structured",
            })
    return normalized


def load_cases(path: str | Path) -> list:
    """
    파일 또는 디렉토리 경로에 따라 자동으로 파서를 선택해 test_cases를 반환.
    디렉토리일 경우 내부의 모든 .md, .json 파일을 파싱해 합산함.

    Args:
        path: .md/.json 파일 경로 또는 디렉토리 경로

    Returns:
        normalize된 test_cases 리스트
    """
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"케이스 파일 혹은 디렉토리 없음: {p}")

    if p.is_dir():
        all_cases = []
        # .md, .json 파일들을 찾아서 정렬 (순서 보장)
        files = sorted(list(p.glob("*.md")) + list(p.glob("*.json")))
        for f in files:
            all_cases.extend(load_cases(f))
        return all_cases

    text = p.read_text(encoding="utf-8")

    if p.suffix == ".md":
        return parse_md(text)
    elif p.suffix == ".json":
        return parse_json(text)
    else:
        raise ValueError(f"지원하지 않는 형식: {p.suffix}  (.md 또는 .json만 지원)")
