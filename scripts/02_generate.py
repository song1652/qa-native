"""
Step 2 — 테스트 코드 뼈대 생성 (템플릿 기반)
LLM 없음. plan을 읽어 코드 뼈대를 생성.
Claude Code가 이 뼈대를 완성해 tests/generated/test_generated.py에 직접 작성.

뼈대 생성 후 Claude Code에게:
  "02_generate.py가 생성한 뼈대를 기반으로
   tests/generated/test_generated.py를 완성해줘.
   실제 셀렉터와 assertion을 plan의 내용대로 채워넣어."
"""
import json
import sys
from pathlib import Path
from _paths import PIPELINE_STATE


CONFTEST_TEMPLATE = '''import pytest
from pathlib import Path
from playwright.sync_api import sync_playwright


@pytest.fixture(scope="session")
def browser_instance():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        yield browser
        browser.close()


@pytest.fixture
def page(browser_instance):
    context = browser_instance.new_context()
    page = context.new_page()
    yield page
    context.close()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        page = item.funcargs.get("page")
        if page:
            shot_dir = Path("tests/screenshots")
            shot_dir.mkdir(parents=True, exist_ok=True)
            path = shot_dir / f"{item.name}.png"
            try:
                page.screenshot(path=str(path))
                print(f"\\n스크린샷 저장: {path}")
            except Exception:
                pass
'''

TEST_FILE_HEADER = '''"""
자동 생성된 Playwright 테스트 코드
URL: {url}
생성 케이스: {case_count}개

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
import pytest
from playwright.sync_api import expect

BASE_URL = "{url}"
'''

TEST_CASE_SCAFFOLD = '''

def test_{func_name}(page):
    """{description}"""
    # TODO: Claude Code가 아래를 완성
    # 케이스 타입: {case_type}
    # 전략: {steps_hint}
    # 검증: {assertion_hint}
    pass
'''


def slugify(text: str) -> str:
    import re
    text = text.lower().strip()
    # 영문, 숫자, 공백/언더스코어만 허용 (한글 제거)
    text = re.sub(r'[^a-z0-9\s_]', '', text)
    text = re.sub(r'[\s]+', '_', text)
    text = text.strip('_')
    return text[:50] if text else "unnamed"


def main():
    state_path = PIPELINE_STATE
    if not state_path.exists():
        print("[오류] state/pipeline.json 없음.")
        sys.exit(1)

    state = json.loads(state_path.read_text(encoding="utf-8"))

    if not state.get("plan"):
        print("[오류] plan 없음. Claude Code가 전략 수립을 먼저 완료해야 합니다.")
        sys.exit(1)

    plan = state["plan"]
    url  = state["url"]

    # conftest.py 생성 (이미 있으면 건너뜀)
    conftest_path = Path("tests/conftest.py")
    if not conftest_path.exists():
        conftest_path.parent.mkdir(parents=True, exist_ok=True)
        conftest_path.write_text(CONFTEST_TEMPLATE, encoding="utf-8")
        print(f"[02] conftest.py 생성: {conftest_path}")
    else:
        print(f"[02] conftest.py 이미 존재 — 건너뜀: {conftest_path}")

    # 테스트 파일 뼈대 생성
    out_dir = Path("tests/generated")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = Path(state["generated_file_path"])

    scaffold = TEST_FILE_HEADER.format(url=url, case_count=len(plan))

    for idx, case in enumerate(plan):
        steps_hint = " → ".join(
            f"{s.get('action','?')}({s.get('selector','?')})"
            for s in case.get("steps", [])
        )
        assertion = case.get("assertion", {})
        if isinstance(assertion, list):
            assertion_hint = " + ".join(f"{a.get('type','?')}: {a.get('expected','?')}" for a in assertion)
        else:
            assertion_hint = f"{assertion.get('type','?')}: {assertion.get('expected','?')}"

        scaffold += TEST_CASE_SCAFFOLD.format(
            func_name=slugify(case.get("case_name", f"case_{idx}")),
            description=case.get("description", case.get("case_name", "")),
            case_type=case.get("case_type", ""),
            steps_hint=steps_hint,
            assertion_hint=assertion_hint,
        )

    out_path.write_text(scaffold, encoding="utf-8")

    state["step"] = "scaffolded"
    state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"[02] 뼈대 생성 완료: {out_path}  ({len(plan)}개 케이스)")
    print()
    print("[다음] Claude Code가 뼈대를 완성합니다.")
    print("       실제 셀렉터와 assertion을 plan 내용대로 채워넣습니다.")


if __name__ == "__main__":
    main()
