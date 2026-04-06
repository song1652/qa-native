"""
자동 생성된 Playwright 테스트 코드
URL: https://the-internet.herokuapp.com/
케이스: tc_44_iframe_content_access (tc_44)

Claude Code가 plan 기반으로 완성한 파일.
수동 편집 가능.
"""
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com/"


def test_iframe_content_access(page):
    """iframe 접근 및 TinyMCE 콘텐츠 확인"""
    # /tinymce (WYSIWYG Editor) 페이지로 직접 이동
    page.goto(BASE_URL + "iframe")
    page.wait_for_load_state("networkidle")

    # URL 확인
    expect(page).to_have_url(BASE_URL + "iframe", timeout=10000)

    # TinyMCE iframe 접근 - lessons: page.evaluate로 접근
    iframe_element = page.locator("iframe#mce_0_ifr")
    expect(iframe_element).to_be_visible(timeout=10000)

    # TinyMCE 콘텐츠 확인 - evaluate로 직접 읽기
    content = page.evaluate(
        """() => {
            const iframe = document.querySelector('iframe#mce_0_ifr');
            if (!iframe) return null;
            const doc = iframe.contentDocument
                || iframe.contentWindow.document;
            const body = doc.querySelector('#tinymce');
            return body ? body.innerText : null;
        }"""
    )
    assert content is not None, "TinyMCE iframe content not accessible"
    assert len(content.strip()) > 0, "TinyMCE content is empty"
