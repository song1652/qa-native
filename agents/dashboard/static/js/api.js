// ── API & Data Fetching ──
async function fetchPipelineState() {
  try {
    const res = await fetch('/api/pipeline_state?' + Date.now());
    if (res.ok) pipelineState = await res.json();
  } catch (e) { }
}

async function fetchBatchState() {
  try {
    const res = await fetch('/api/batch_state?' + Date.now());
    if (res.ok) batchState = await res.json();
  } catch (e) { }
}

async function fetchReports() {
  try {
    const res = await fetch('/api/reports?' + Date.now());
    if (res.ok) reportsList = await res.json();
  } catch (e) { }
}

async function fetchPages() {
  try {
    const res = await fetch('/api/pages?' + Date.now());
    if (res.ok) pagesData = await res.json();
  } catch (e) { }
}

async function fetchGeneratedGroups() {
  try {
    const res = await fetch('/api/generated_groups?' + Date.now());
    if (res.ok) generatedGroups = await res.json();
  } catch (e) { }
}

async function fetchQuickState() {
  try {
    const res = await fetch('/api/quick_state?' + Date.now());
    if (res.ok) quickState = await res.json();
  } catch (e) { }
}

function _shouldSkipRender() {
  // 사용자가 select/input 조작 중이면 스킵
  const mainEl = document.getElementById('main');
  if (mainEl && mainEl.contains(document.activeElement)
    && (document.activeElement.tagName === 'SELECT' || document.activeElement.tagName === 'INPUT')) {
    return true;
  }
  // iframe이 열려 있으면 스킵 (리포트 보는 중)
  const reportWrap = document.getElementById('report-iframe-wrap');
  if (reportWrap && reportWrap.style.display !== 'none') return true;
  const parallelReportWrap = document.getElementById('parallel-report-wrap');
  if (parallelReportWrap && parallelReportWrap.style.display !== 'none') return true;
  const singleReportWrap = document.getElementById('single-report-wrap');
  if (singleReportWrap && singleReportWrap.style.display !== 'none') return true;
  // 빠른 실행 중 로그 폴링 시 DOM 재생성 방지
  if (currentView === 'quick_run' && _quickRunState.running) return true;
  return false;
}

function _saveScrollPos() {
  const scroll = document.querySelector('.content-scroll');
  if (scroll && currentView) _uiState.scrollTop[currentView] = scroll.scrollTop;
}

function _restoreScrollPos() {
  const scroll = document.querySelector('.content-scroll');
  if (scroll && currentView && _uiState.scrollTop[currentView]) {
    scroll.scrollTop = _uiState.scrollTop[currentView];
  }
}

async function refreshAll() {
  await Promise.all([
    fetch('/api/dialogs?' + Date.now()).then(r => r.ok ? r.text() : null).then(t => { if (t) applyDialogData(t); }),
    fetchPipelineState(),
    fetchBatchState(),
    fetchReports(),
    fetchPages(),
    fetchGeneratedGroups(),
    fetchQuickState(),
  ]);
  updateSidebar(lastData || {});
  if (!_shouldSkipRender()) {
    _saveScrollPos();
    renderCurrentView();
    _restoreScrollPos();
  }
}

// SSE — state/pipeline.json 변경 시 파이프라인 상태도 즉시 갱신
function connectSSE() {
  const es = new EventSource('/api/events');
  es.onmessage = async e => {
    applyDialogData(e.data);
    await fetchPipelineState();
    await fetchBatchState();
    if (!_shouldSkipRender()) {
      _saveScrollPos();
      renderCurrentView();
      _restoreScrollPos();
    }
  };
  es.onerror = () => { es.close(); setTimeout(connectSSE, 5000); };
}

function applyDialogData(text) {
  if (text === lastJson) return;
  lastJson = text;
  lastData = JSON.parse(text);
  refreshCount++;
  const now = new Date().toLocaleTimeString('ko-KR', { hour12: false });
  document.getElementById('header-meta').textContent = `${now} · ${refreshCount}회`;
  updateSidebar(lastData);
  if (currentView.startsWith('team_') || currentView === '') renderCurrentView();
}
