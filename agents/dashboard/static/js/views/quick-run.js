// ── Quick Run View ──
function renderQuickRun(main) {
  // 체크 상태 보존
  const prevChecked = {};
  document.querySelectorAll('.quick-group-cb').forEach(cb => { prevChecked[cb.value] = cb.checked; });

  const groups = generatedGroups || [];
  const execResult = quickState ? quickState.execution_result : null;

  let groupsHtml = '';
  if (groups.length) {
    groupsHtml = groups.map(g => {
      const checked = prevChecked[g.name] !== undefined ? prevChecked[g.name] : true;
      return `<label class="quick-group-item">
        <input type="checkbox" class="quick-group-cb" value="${esc(g.name)}" ${checked ? 'checked' : ''}>
        <span class="quick-group-name">${esc(g.name)}</span>
        <span class="quick-group-count">${g.file_count}개 파일</span>
      </label>`;
    }).join('');
  } else {
    groupsHtml = '<div style="padding:12px;font-size:13px;color:var(--text-dim);">생성된 테스트 폴더가 없습니다. 먼저 병렬 파이프라인으로 테스트 코드를 생성하세요.</div>';
  }

  // 실행 결과 카드
  let resultHtml = '';
  if (execResult) {
    const allPass = execResult.failed === 0;
    const badgeCls = allPass ? 'pass' : 'fail';
    const badgeTxt = allPass ? 'ALL PASS' : `${execResult.failed} FAILED`;
    const groupResultsHtml = buildGroupResultsHtml(execResult.group_results || {}, 'quick');
    resultHtml = `
      <div class="exec-result-card">
        <div class="exec-result-header">
          <span class="exec-result-title">실행 결과</span>
          <span class="exec-result-badge ${badgeCls}">${badgeTxt}</span>
        </div>
        <div class="exec-result-stats">
          <div class="exec-stat"><div class="exec-stat-num" style="color:var(--text)">${execResult.total}</div><div class="exec-stat-label">Total</div></div>
          <div class="exec-stat"><div class="exec-stat-num" style="color:var(--approved-color)">${execResult.passed}</div><div class="exec-stat-label">Passed</div></div>
          <div class="exec-stat"><div class="exec-stat-num" style="color:var(--revision-color)">${execResult.failed}</div><div class="exec-stat-label">Failed</div></div>
          <div class="exec-stat"><div class="exec-stat-num" style="color:${allPass ? 'var(--approved-color)' : 'var(--revision-color)'}">${execResult.pass_rate}%</div><div class="exec-stat-label">Pass Rate</div></div>
        </div>
        ${groupResultsHtml}
        <div style="margin-top:12px;font-size:11px;color:var(--text-dim);">
          실행: ${esc(execResult.executed_at || '')} | 힐링: ${execResult.heal_count || 0}회
          ${execResult.report_name ? ` | <a href="/reports/${esc(execResult.report_name)}" target="_blank" style="color:var(--senior-accent);text-decoration:none;">리포트 보기</a>` : ''}
        </div>
      </div>`;
  }

  const logVis = _quickRunState.logVisible;
  main.innerHTML = `
    <div class="pipeline-view">
      <div class="pipeline-title">빠른 실행</div>
      <p style="font-size:12px;color:var(--text-dim);margin-bottom:16px;">
        tests/generated/ 에 이미 생성된 테스트 코드를 바로 실행합니다. 전체 파이프라인을 거치지 않습니다.
      </p>
      <div style="background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:16px;margin-bottom:16px;">
        <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:12px;">
          <span style="font-size:13px;font-weight:600;">테스트 폴더 선택</span>
          <label style="font-size:12px;color:var(--text-dim);cursor:pointer;display:flex;align-items:center;gap:4px;">
            <input type="checkbox" id="quick-select-all" onchange="quickToggleAll(this.checked)" checked>
            전체 선택
          </label>
        </div>
        <div class="quick-group-list">${groupsHtml}</div>
        <div style="display:flex;gap:10px;align-items:center;margin-top:14px;">
          <button class="action-btn action-btn-primary" id="quick-run-btn" onclick="runQuickTest()" ${!groups.length ? 'disabled' : ''}>
            ${_quickRunState.running ? '실행 중...' : '테스트 실행'}
          </button>
          <label style="font-size:12px;color:var(--text-dim);cursor:pointer;display:flex;align-items:center;gap:4px;">
            <input type="checkbox" id="quick-no-heal"> 힐링 생략
          </label>
          ${!groups.length ? '<span style="font-size:11px;color:var(--danger);">tests/generated/ 에 생성된 테스트가 없습니다</span>' : ''}
        </div>
      </div>
      <div class="run-log-box" id="run-quick-log" style="display:${logVis ? 'block' : 'none'};margin-bottom:16px;">
        <pre id="run-quick-log-content" style="margin:0;">${esc(_quickRunState.logContent || '(대기 중...)')}</pre>
      </div>
      <button class="log-toggle-btn" id="log-toggle-quick" onclick="toggleLogExpand('run-quick-log')" style="display:${logVis ? 'inline-block' : 'none'};margin-bottom:16px;">확대</button>
      ${resultHtml}
      <div style="display:flex;justify-content:flex-end;margin-top:16px;">
        <button class="action-btn action-btn-danger" onclick="quickReset()">빠른 실행 초기화</button>
      </div>
    </div>`;

  // 체크 상태 복원 후 전체선택 체크박스 상태 동기화
  const allCb = document.getElementById('quick-select-all');
  const cbs = document.querySelectorAll('.quick-group-cb');
  if (allCb && cbs.length) {
    allCb.checked = Array.from(cbs).every(cb => cb.checked);
  }
}

function quickToggleAll(checked) {
  document.querySelectorAll('.quick-group-cb').forEach(cb => { cb.checked = checked; });
}

async function runQuickTest() {
  const cbs = document.querySelectorAll('.quick-group-cb:checked');
  const groups = Array.from(cbs).map(cb => cb.value);
  if (!groups.length) { showToast('실행할 폴더를 선택하세요', 'info'); return; }

  const btn = document.getElementById('quick-run-btn');
  _quickRunState.running = true;
  _quickRunState.logContent = '';
  // 이전 실행 결과 클리어 (서버 + 클라이언트 모두)
  quickState = {};
  try { await fetch('/api/quick/reset', { method: 'POST' }); } catch (e) {}
  if (btn) { btn.textContent = '실행 중...'; btn.disabled = true; }
  // 결과 카드 즉시 제거
  const oldResult = document.querySelector('.exec-result-card');
  if (oldResult) oldResult.remove();

  try {
    const res = await fetch('/api/run_quick', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ groups, no_heal: !!document.getElementById('quick-no-heal')?.checked }),
    });
    const data = await res.json();
    if (data.ok) {
      if (btn) btn.textContent = '실행됨 (PID: ' + (data.pid || '?') + ')';
      _quickRunState.logVisible = true;
      startLogPolling('run-quick-log', 'run-quick-log-content', 'quick_run.txt');
      // 완료 대기 → 결과 자동 갱신
      const checkDone = setInterval(async () => {
        await fetchQuickState();
        const qs = quickState || {};
        if (qs.status === 'done' || qs.status === 'heal_needed' || qs.status === 'heal_failed') {
          clearInterval(checkDone);
          // 로그 폴링 정리 + 최종 로그 보존
          if (_logTimers['run-quick-log']) {
            clearInterval(_logTimers['run-quick-log']);
            delete _logTimers['run-quick-log'];
          }
          const logEl = document.getElementById('run-quick-log-content');
          if (logEl) _quickRunState.logContent = logEl.textContent;
          _quickRunState.running = false;
          if (currentView === 'quick_run' && !_confirmOpen) renderQuickRun(document.getElementById('main'));
          if (btn) { btn.textContent = '테스트 실행'; btn.disabled = false; }
        }
      }, 3000);
      // 최대 5분 후 자동 해제
      setTimeout(() => {
        clearInterval(checkDone);
        _quickRunState.running = false;
        if (btn) { btn.textContent = '테스트 실행'; btn.disabled = false; }
      }, 300000);
    } else {
      showToast('오류: ' + (data.error || 'unknown'));
      _quickRunState.running = false;
      if (btn) { btn.textContent = '테스트 실행'; btn.disabled = false; }
    }
  } catch (e) {
    showToast('서버 연결 오류');
    _quickRunState.running = false;
    if (btn) { btn.textContent = '테스트 실행'; btn.disabled = false; }
  }
}

async function quickReset() {
  if (!(await safeConfirm('빠른 실행 상태를 초기화하시겠습니까?'))) return;
  try {
    const res = await fetch('/api/quick/reset', { method: 'POST' });
    const data = await res.json();
    if (data.ok) {
      _quickRunState = { running: false, logVisible: false, logContent: '' };
      showToast('빠른 실행 초기화 완료', 'success');
      await refreshAll();
    } else {
      showToast('초기화 실패: ' + (data.error || ''));
    }
  } catch (e) { showToast('서버 연결 오류'); }
}
