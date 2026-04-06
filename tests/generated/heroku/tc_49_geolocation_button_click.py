"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_49_geolocation_button_click (tc_49)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"


def test_geolocation_button_click(page):
    """Geolocation 위치 정보 버튼 클릭"""
    page.goto(BASE_URL + "geolocation")
    page.wait_for_load_state("networkidle")

    # JS로 geolocation API를 직접 모킹 (grant_permissions asyncio 충돌 회피)
    page.evaluate("""
        () => {
            const mockCoords = {
                latitude: 37.5665,
                longitude: 126.9780,
                accuracy: 100
            };
            navigator.geolocation.getCurrentPosition = function(success) {
                success({ coords: mockCoords });
            };
        }
    """)

    # "Where am I?" 버튼 확인 및 클릭
    button = page.locator("button", has_text="Where am I?")
    expect(button).to_be_visible(timeout=10000)
    button.click()

    # 위치 정보 결과가 #demo에 표시될 때까지 대기
    demo = page.locator("#demo")
    expect(demo).not_to_be_empty(timeout=10000)

    demo_text = demo.inner_text()
    assert "Latitude" in demo_text or "latitude" in demo_text, (
        f"Expected latitude info in demo, got: {demo_text}"
    )
