# Lessons Learned (Auto) — 자동 기록 힐링 패턴

> **자동 생성 파일**: `heal_utils.py`의 `append_lessons()`가 힐링 시 자동 기록.
> 수동 큐레이션 패턴은 [lessons_learned.md](lessons_learned.md) 참조.

---

## Locator 오류

- **Locator**: `expect(sub_items.first).to_be_visible(timeout=5000)` — dom_info 셀렉터 재확인, #id 우선 사용
- **Locator**: `expect(submenu.first).to_be_visible(timeout=5000)` — dom_info 셀렉터 재확인, #id 우선 사용
- **Locator**: `expect(disabled_option).to_be_visible(timeout=5000)` — dom_info 셀렉터 재확인, #id 우선 사용
- **Locator**: `expect(prevent_tab).to_be_visible(timeout=10000)` — dom_info 셀렉터 재확인, #id 우선 사용
- **Locator**: `await self._channel.send("click", self._timeout, locals_to_params(locals()))` — dom_info 셀렉터 재확인, #id 우선 사용
- **Locator**: `expect(table_body).to_be_visible(timeout=5000)` — dom_info 셀렉터 재확인, #id 우선 사용
- **Locator**: `expect(page.locator("input[value='Sports']")).to_be_checked(timeout=5000)` — dom_info 셀렉터 재확인, #id 우선 사용
- **Locator**: `return await self._channel.send("selectOption", self._timeout, params)` — dom_info 셀렉터 재확인, #id 우선 사용
- **Locator**: `self._sync(self._impl_obj.get_attribute(name=name, timeout=timeout))` — dom_info 셀렉터 재확인, #id 우선 사용
- **Locator**: `expect(selected).to_be_visible(timeout=10000)` — dom_info 셀렉터 재확인, #id 우선 사용
- **Locator**: `expect(drop_here).to_contain_text("Drop here", timeout=5000)` — dom_info 셀렉터 재확인, #id 우선 사용
- **Locator**: `expect(sub_item).to_be_visible(timeout=10000)` — dom_info 셀렉터 재확인, #id 우선 사용
- **Locator**: `expect(sub_sub_list).to_be_visible(timeout=10000)` — dom_info 셀렉터 재확인, #id 우선 사용
- **Locator**: `expect(container).to_be_visible(timeout=5000)` — dom_info 셀렉터 재확인, #id 우선 사용
- **Locator**: `expect(acceptable).to_be_visible(timeout=5000)` — dom_info 셀렉터 재확인, #id 우선 사용
- **Locator**: `expect(first_option).to_be_visible(timeout=10000)` — dom_info 셀렉터 재확인, #id 우선 사용
- **Locator**: `expect(page.locator(".main-header")).to_contain_text("Check Box", timeout=5000)` — dom_info 셀렉터 재확인, #id 우선 사용
- **Locator**: `expect(first_name).to_have_class(re.compile(r"field-error"), timeout=5000)` — dom_info 셀렉터 재확인, #id 우선 사용
- **Locator**: `expect(col_b_header).to_have_text("A", timeout=5000)` — dom_info 셀렉터 재확인, #id 우선 사용
- **Locator**: `expect(modal).to_be_visible(timeout=10000)` — dom_info 셀렉터 재확인, #id 우선 사용
- **Locator**: `assert is_in_viewport, "Floating menu is not visible in viewport after scroll"` — dom_info 셀렉터 재확인, #id 우선 사용
- **Locator**: `expect(col_a_header).to_have_text("B", timeout=5000)` — dom_info 셀렉터 재확인, #id 우선 사용
- **Locator**: `E   AssertionError: Locator expected to be visible` — dom_info 셀렉터 재확인, #id 우선 사용
- **Locator**: `expect(not_greedy_inner).to_contain_text("Dropped!", timeout=5000)` — dom_info 셀렉터 재확인, #id 우선 사용
- **Locator**: `expect(drop_target).to_contain_text("Dropped!", timeout=5000)` — dom_info 셀렉터 재확인, #id 우선 사용
- **Locator**: `expect(page.locator("#result")).to_contain_text("You entered: ENTER", timeout=5000)` — dom_info 셀렉터 재확인, #id 우선 사용
- **Locator**: `expect(page.locator("p")).to_be_visible(timeout=5000)` — dom_info 셀렉터 재확인, #id 우선 사용
- **Locator**: `expect(cell).to_have_text("50.1")` — dom_info 셀렉터 재확인, #id 우선 사용
- **Locator**: `expect(page.locator("a", has_text="Downloads")).to_be_visible(timeout=5000)` — dom_info 셀렉터 재확인, #id 우선 사용
- **Locator**: `expect(img).to_be_visible(timeout=5000)` — dom_info 셀렉터 재확인, #id 우선 사용
- **Locator**: `assert items.count() >= 5, f"Expected at least 5 list items, got {items.count()}"` — dom_info 셀렉터 재확인, #id 우선 사용
- **Locator**: `expect(page.locator("div.tox-toolbar, div.mce-toolbar")).to_be_visible(timeout=10000)` — dom_info 셀렉터 재확인, #id 우선 사용
- **Locator**: `assert toolbar.count() > 0, "TinyMCE toolbar should be present"` — dom_info 셀렉터 재확인, #id 우선 사용
- **Locator**: `expect(img).to_be_visible(timeout=10000)` — dom_info 셀렉터 재확인, #id 우선 사용

## Assertion 오류

- **Assertion**: `assert idx_one > idx_three, f"Expected 'One' after 'Three', got order: {texts}"` — 실제 페이지 텍스트/상태로 기댓값 수정
- **Assertion**: `assert "In a list!" in text, f"Expected 'In a list!' in shadow DOM text, got: {text!r}"` — 실제 페이지 텍스트/상태로 기댓값 수정
- **Assertion**: `assert count >= 5, f"Expected at least 5 list items, got {count}"` — 실제 페이지 텍스트/상태로 기댓값 수정
- **Assertion**: `E   AssertionError: Width should increase` — 실제 페이지 텍스트/상태로 기댓값 수정
- **Assertion**: `assert "In a list!" in text or "list" in text.lower(), f"Expected list content, got: {text}"` — 실제 페이지 텍스트/상태로 기댓값 수정

## Timeout 오류

## URL 오류

## JS평가 오류

## Python런타임 오류

## Playwright일반 오류

- **Playwright일반**: `raise Error(` — 브라우저 상태 확인, 페이지 닫힘/크래시 대응

## 기타
