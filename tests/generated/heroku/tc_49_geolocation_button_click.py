"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_49_geolocation_button_click (tc_49)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from pathlib import Path
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_DATA_PATH = PROJECT_ROOT / "config" / "test_data.json"


def test_tc_49_geolocation_button_click(page):
    """Where am I? 버튼 클릭 후 위도/경도 정보 표시 확인 (geolocation 모킹 필요)"""
    page.goto("https://the-internet.herokuapp.com/geolocation")
    page.wait_for_load_state("domcontentloaded")

    # Mock navigator.geolocation via page.evaluate (avoid grant_permissions asyncio conflict)
    page.evaluate(
        """() => {
            const mockGeolocation = {
                getCurrentPosition: (success) => {
                    success({
                        coords: {
                            latitude: 37.5665,
                            longitude: 126.9780,
                            accuracy: 10
                        }
                    });
                },
                watchPosition: () => {}
            };
            Object.defineProperty(navigator, 'geolocation', {
                value: mockGeolocation,
                writable: true,
                configurable: true
            });
        }"""
    )

    page.locator("button", has_text="Where am I?").click()

    # Verify latitude and longitude are displayed
    lat = page.locator("#lat-value")
    lng = page.locator("#long-value")
    expect(lat).to_be_visible(timeout=10000)
    expect(lng).to_be_visible(timeout=10000)

    lat_text = lat.inner_text()
    lng_text = lng.inner_text()
    assert lat_text != ""
    assert lng_text != ""
