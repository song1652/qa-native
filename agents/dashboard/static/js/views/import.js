// ── Import (Excel → tc_*.md) ──
async function loadImportFiles() {
  try {
    const res = await fetch('/api/import/files');
    const data = await res.json();
    const sel = document.getElementById('import-file-select');
    if (!sel) return;
    const prev = sel.value;
    sel.innerHTML = '<option value="">파일 선택...</option>';
    (data.files || []).forEach(f => {
      sel.innerHTML += `<option value="${esc(f)}">${esc(f)}</option>`;
    });
    if (prev) sel.value = prev;
  } catch (e) { }
}

async function onImportFileSelect() {
  const sel = document.getElementById('import-file-select');
  const listEl = document.getElementById('import-sheet-list');
  const btn = document.getElementById('import-convert-btn');
  const statusEl = document.getElementById('import-status');
  const resultsEl = document.getElementById('import-results');
  listEl.innerHTML = ''; btn.disabled = true;
  statusEl.textContent = ''; statusEl.className = 'import-status';
  resultsEl.innerHTML = '';
  const file = sel.value;
  if (!file) return;
  statusEl.textContent = '시트 분석 중...';
  try {
    const res = await fetch(`/api/import/sheets?file=${encodeURIComponent(file)}`);
    const data = await res.json();
    if (!data.ok) { statusEl.textContent = data.error || '분석 실패'; statusEl.className = 'import-status err'; return; }
    const sheets = data.sheets || [];
    if (!sheets.length) { statusEl.textContent = '변환 가능한 시트 없음'; statusEl.className = 'import-status err'; return; }
    statusEl.textContent = `${sheets.length}개 시트 발견`;
    listEl.innerHTML = `<label class="import-sheet-item" style="border-bottom:1px solid var(--border);padding-bottom:8px;margin-bottom:4px;">
      <input type="checkbox" id="import-select-all" onchange="importToggleAll(this.checked)" checked>
      <span class="import-sheet-name" style="font-weight:600;">전체 선택</span>
    </label>` + sheets.map(s => `<label class="import-sheet-item">
      <input type="checkbox" class="import-sheet-cb" value="${esc(s.name)}" checked>
      <span class="import-sheet-name">${esc(s.name)}</span>
      <span class="import-sheet-count">${s.count}건</span>
    </label>`).join('');
    btn.disabled = false;
  } catch (e) { statusEl.textContent = '서버 연결 오류'; statusEl.className = 'import-status err'; }
}

function importToggleAll(checked) {
  document.querySelectorAll('.import-sheet-cb').forEach(cb => { cb.checked = checked; });
}

async function runImportConvert() {
  const file = document.getElementById('import-file-select').value;
  const cbs = document.querySelectorAll('.import-sheet-cb:checked');
  const sheets = Array.from(cbs).map(cb => cb.value);
  const btn = document.getElementById('import-convert-btn');
  const statusEl = document.getElementById('import-status');
  const resultsEl = document.getElementById('import-results');
  if (!file || !sheets.length) { showToast('시트를 선택하세요', 'info'); return; }
  btn.disabled = true; btn.textContent = '변환 중...';
  statusEl.textContent = ''; resultsEl.innerHTML = '';
  try {
    const res = await fetch('/api/import/convert', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ file, sheets })
    });
    const data = await res.json();
    if (data.ok) {
      const total = (data.results || []).reduce((s, r) => s + (r.count || 0), 0);
      statusEl.textContent = `변환 완료: 총 ${total}건`;
      statusEl.className = 'import-status ok';
      resultsEl.innerHTML = (data.results || []).map(r =>
        `<div class="import-result-item">${esc(r.sheet)}: <span class="count">${r.count}건</span> → ${esc(r.folder || '')}</div>`
      ).join('');
      showToast(`${sheets.length}개 시트, ${total}건 변환 완료`, 'success');
    } else {
      statusEl.textContent = data.error || '변환 실패';
      statusEl.className = 'import-status err';
    }
  } catch (e) { statusEl.textContent = '서버 연결 오류'; statusEl.className = 'import-status err'; }
  btn.disabled = false; btn.textContent = '변환';
}
