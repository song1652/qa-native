// ── Test List: Filter + Pagination (공통) ──
function _getTestListKey(prefix, groupName) { return prefix + '__' + (groupName || 'all'); }

function _getState(key) {
  if (!_testListState[key]) _testListState[key] = { filter: 'all', page: 1 };
  return _testListState[key];
}

function testListSetFilter(prefix, groupName, filter) {
  const st = _getState(_getTestListKey(prefix, groupName));
  st.filter = filter;
  st.page = 1;
  refreshAll();
}

function testListSetPage(prefix, groupName, page) {
  const st = _getState(_getTestListKey(prefix, groupName));
  st.page = page;
  refreshAll();
}

function buildTestListHtml(tests, prefix, groupName) {
  if (!tests || !tests.length) return '';
  const key = _getTestListKey(prefix, groupName);
  const st = _getState(key);
  const filter = st.filter;
  const filtered = filter === 'all' ? tests : tests.filter(t => filter === 'pass' ? t.passed : !t.passed);
  const totalPages = Math.max(1, Math.ceil(filtered.length / TESTS_PER_PAGE));
  const page = Math.min(st.page, totalPages);
  const start = (page - 1) * TESTS_PER_PAGE;
  const pageItems = filtered.slice(start, start + TESTS_PER_PAGE);
  const passCount = tests.filter(t => t.passed).length;
  const failCount = tests.length - passCount;

  const pfx = esc(prefix);
  const gn = esc(groupName || '');
  let html = '<div class="test-list-controls">';
  html += `<button class="test-filter-btn ${filter === 'all' ? 'active-all' : ''}" onclick="testListSetFilter('${pfx}','${gn}','all')">All (${tests.length})</button>`;
  html += `<button class="test-filter-btn ${filter === 'pass' ? 'active-pass' : ''}" onclick="testListSetFilter('${pfx}','${gn}','pass')">Pass (${passCount})</button>`;
  html += `<button class="test-filter-btn ${filter === 'fail' ? 'active-fail' : ''}" onclick="testListSetFilter('${pfx}','${gn}','fail')">Fail (${failCount})</button>`;
  if (totalPages > 1) {
    html += `<div class="test-list-pager">`;
    html += `<button onclick="testListSetPage('${pfx}','${gn}',${page - 1})" ${page <= 1 ? 'disabled' : ''}>&laquo;</button>`;
    html += `<span>${page} / ${totalPages}</span>`;
    html += `<button onclick="testListSetPage('${pfx}','${gn}',${page + 1})" ${page >= totalPages ? 'disabled' : ''}>&raquo;</button>`;
    html += `</div>`;
  }
  html += '</div>';

  html += '<table class="test-list-table"><thead><tr><th style="width:30px">#</th><th>테스트</th><th style="width:80px">상태</th></tr></thead><tbody>';
  pageItems.forEach((t, i) => {
    const num = start + i + 1;
    const cls = t.passed ? 'pass' : 'fail';
    const label = t.passed ? 'PASS' : 'FAIL';
    html += `<tr><td style="color:var(--text-dim)">${num}</td><td>${esc(t.name)}</td><td style="white-space:nowrap"><span class="test-status-dot ${cls}"></span>${label}</td></tr>`;
  });
  html += '</tbody></table>';
  return html;
}
