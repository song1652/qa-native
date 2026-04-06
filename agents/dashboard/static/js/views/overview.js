// ── Dashboard Overview ──
async function _loadOverviewData() {
  try {
    const [rh, hs] = await Promise.all([
      fetch('/api/run_history').then(r => r.json()),
      fetch('/api/heal_stats').then(r => r.json()),
    ]);
    _ovRunHistory = rh || [];
    _ovHealStats = hs || {};
  } catch(e) { _ovRunHistory = []; _ovHealStats = {}; }
}

async function renderDashboardOverview(main) {
  await _loadOverviewData();

  // ── 데이터 수집 ──
  const ps = pipelineState || {};
  const psStep = ps.step || '-';
  const psStatus = ps.status || (psStep === 'done' ? 'done' : (psStep !== '-' && psStep !== 'init' ? 'running' : 'idle'));
  const psResult = ps.execution_result || {};
  const psPassed = psResult.passed || 0;
  const psFailed = psResult.failed || 0;
  const psTotal = psResult.total || 0;

  const bs = (batchState || {}).parallel_state || {};
  const bsStatus = bs.status || (bs.step === 'done' ? 'done' : 'idle');
  const bsResult = bs.execution_result || {};
  const bsPassed = bsResult.passed || 0;
  const bsFailed = bsResult.failed || 0;
  const bsTotal = bsResult.total || 0;

  const rptCount = (reportsList || []).length;
  const history = _ovRunHistory || [];
  const healStats = _ovHealStats || {};
  const patterns = healStats.patterns || {};

  // 최근 실행 결과 (run_history 마지막 1건)
  const lastRun = history.length > 0 ? history[history.length - 1] : null;
  const totalTests = lastRun ? (lastRun.total || 0) : 0;
  const totalPassed = lastRun ? (lastRun.passed || 0) : 0;
  const totalFailed = lastRun ? (lastRun.failed || 0) : 0;
  const passRate = totalTests > 0 ? Math.round(totalPassed / totalTests * 100) : 0;
  const lastRunLabel = lastRun ? ({parallel:'병렬', quick:'빠른 실행', single:'단일'}[lastRun.pipeline] || lastRun.pipeline) + ' · ' + (lastRun.timestamp || '').split(' ')[1] || '' : '';

  // 그룹별 커버리지
  const groups = pagesData.groups || [];
  const genGroups = generatedGroups || [];
  let coverageHtml = '';
  if (groups.length > 0) {
    const coverageRows = groups.map(g => {
      const gen = genGroups.find(gg => gg.name === g.name);
      const genCount = gen ? gen.file_count : 0;
      const caseCount = g.count || 0;
      const pct = caseCount > 0 ? Math.round(genCount / caseCount * 100) : 0;
      const barColor = pct === 100 ? 'var(--approved-color)' : pct > 0 ? 'var(--pending-color)' : 'var(--text-dim)';
      return `<div class="cov-row">
            <div class="cov-top"><span class="cov-name">${esc(g.name)}</span><span class="cov-nums">${genCount}/${caseCount}</span></div>
            <div class="cov-bottom"><div class="cov-bar-track"><div class="cov-bar-fill" style="width:${pct}%;background:${barColor}"></div></div><div class="cov-pct" style="color:${barColor}">${pct}%</div></div>
          </div>`;
    }).join('');
    coverageHtml = `
          <div class="ov-section">
            <div class="ov-section-title">Test Coverage</div>
            ${coverageRows}
          </div>`;
  }

  // 실행 이력 (최근 10개)
  let historyHtml = '';
  if (history.length > 0) {
    const recent = history.slice(-10);
    const bars = recent.map(h => {
      const r = h.pass_rate || 0;
      const color = r === 100 ? 'var(--approved-color)' : r >= 80 ? 'var(--pending-color)' : 'var(--revision-color)';
      const ts = (h.timestamp || '').split(' ')[1] || '';
      const shortTs = ts.substring(0, 5);
      const rInt = Math.round(r);
      const pLabel = {parallel:'병렬', quick:'빠른', single:'단일'}[h.pipeline] || h.pipeline || '';
      return `<div class="trend-col">
            <div class="trend-pct" style="color:${color}">${rInt}%</div>
            <div class="trend-bar" style="height:${Math.max(r, 5)}%;background:${color}" title="${h.timestamp} — ${pLabel} ${r}% (${h.passed}/${h.total})"></div>
            <div class="trend-label">${shortTs}</div>
          </div>`;
    }).join('');
    const lastRun = recent[recent.length - 1];
    const duration = lastRun.duration_sec ? Math.round(lastRun.duration_sec) + 's' : '-';
    const firstPass = lastRun.first_pass ? 'First Pass' : lastRun.heal_count + '회 힐링';
    historyHtml = `
          <div class="ov-section">
            <div class="ov-section-title">Run History</div>
            <div class="trend-chart">${bars}</div>
            <div class="trend-meta">최근 실행: ${duration} · ${firstPass}</div>
          </div>`;
  }

  // Quick Actions
  const hasFailures = totalFailed > 0;
  const hasReports = rptCount > 0;
  let quickHtml = `
        <div class="ov-section">
          <div class="ov-section-title">Quick Actions</div>
          <div class="cmd-grid">
            <div class="cmd-btn" onclick="selectView('parallel_pipeline')">병렬 테스트</div>
            <div class="cmd-btn" onclick="selectView('single_pipeline')">단일 테스트</div>
            ${hasReports ? '<div class="cmd-btn" onclick="selectView(\'reports\')">리포트 보기</div>' : ''}
            <div class="cmd-btn" onclick="selectView('quick_run')">빠른 실행</div>
          </div>
        </div>`;

  // 상태 라벨
  function sLabel(s) {
    if (s === 'done') return '완료';
    if (s === 'idle') return '대기';
    if (s === 'testing') return '실행 중';
    if (s === 'generating') return '생성 중';
    if (s === 'ready') return '준비됨';
    return s;
  }
  function sColor(s) {
    if (s === 'done') return 'var(--approved-color)';
    if (s === 'idle') return 'var(--text-dim)';
    return 'var(--pending-color)';
  }

  // HUD 카드
  const hudHtml = `
        <div class="hud-grid">
          <div class="hud-card" onclick="selectView('single_pipeline')">
            <div class="hud-label">Single Pipeline</div>
            <div class="hud-value" style="color:${sColor(psStatus)}">${sLabel(psStatus)}</div>
            <div class="hud-meta">${psStatus === 'done' && psTotal > 0 ? psPassed + '/' + psTotal + ' passed · ' + Math.round(psPassed/psTotal*100) + '%' : psStep !== '-' && psStep !== 'done' && psStep !== 'init' ? '단계: ' + psStep : '실행 대기'}</div>
          </div>
          <div class="hud-card" onclick="selectView('parallel_pipeline')">
            <div class="hud-label">Parallel Pipeline</div>
            <div class="hud-value" style="color:${sColor(bsStatus)}">${sLabel(bsStatus)}</div>
            <div class="hud-meta">${bsStatus === 'done' && bsTotal > 0 ? bsPassed + '/' + bsTotal + ' passed' : '실행 대기'}</div>
          </div>
          <div class="hud-card" onclick="selectView('reports')">
            <div class="hud-label">Reports</div>
            <div class="hud-value">${rptCount}<span style="font-size:14px;opacity:0.4;margin-left:4px;">건</span></div>
            <div class="hud-meta">${rptCount > 0 ? '최근: ' + esc(reportsList[0].name).substring(0, 28) : '리포트 없음'}</div>
          </div>
        </div>`;

  // 메인 2단 레이아웃
  const leftCol = `
        ${totalTests > 0 ? `
        <div class="ov-section">
          <div class="ov-section-title">
            최근 실행 결과 <span style="font-weight:400;font-size:11px;color:var(--text-dim);margin-left:6px;">${lastRunLabel}</span>
            <span class="status-badge ${totalFailed === 0 ? 'status-approved' : 'status-in_progress'}" style="margin-left:auto;font-size:10px;">${totalFailed === 0 ? 'ALL PASS' : totalFailed + ' FAILED'}</span>
          </div>
          <div class="ov-progress-track"><div class="ov-progress-fill${totalFailed > 0 ? ' ov-progress-fill--warn' : ''}" style="width:${passRate}%"></div></div>
          <div class="ov-results-grid">
            <div class="ov-stat"><div class="ov-stat-num">${totalTests}</div><div class="ov-stat-label">Total</div></div>
            <div class="ov-stat"><div class="ov-stat-num" style="color:var(--approved-color)">${totalPassed}</div><div class="ov-stat-label">Passed</div></div>
            <div class="ov-stat"><div class="ov-stat-num" style="color:var(--revision-color)">${totalFailed}</div><div class="ov-stat-label">Failed</div></div>
            <div class="ov-stat"><div class="ov-stat-num" style="color:${totalFailed === 0 ? 'var(--approved-color)' : 'var(--pending-color)'}">${passRate}%</div><div class="ov-stat-label">Pass Rate</div></div>
          </div>
        </div>` : ''}
        ${coverageHtml}`;

  const rightCol = `${historyHtml}${quickHtml}`;

  // 로그 뷰어
  const logHtml = `
        <div class="ov-section" style="margin-top:20px;">
          <div class="ov-section-title">
            Recent Logs
            <div style="margin-left:auto;display:flex;gap:6px;align-items:center;">
              <button class="ov-log-tab active" data-log="run_qa.txt">단일</button>
              <button class="ov-log-tab" data-log="run_parallel.txt">병렬</button>
              <button class="ov-log-tab" data-log="quick_run.txt">빠른</button>
              <button class="ov-log-refresh" id="ov-log-refresh" title="새로고침">&#8635;</button>
            </div>
          </div>
          <div class="ov-log-box" id="ov-log-content">로그 로딩 중...</div>
        </div>`;

  // 웰컴 뷰 (데이터 없을 때)
  const hasAnyData = totalTests > 0 || history.length > 0 || groups.length > 0;
  const welcomeHtml = !hasAnyData ? `
        <div class="ov-section" style="text-align:center;padding:48px 24px;">
          <div style="font-size:40px;margin-bottom:16px;">🚀</div>
          <h3 style="font-family:'Outfit',sans-serif;font-size:20px;font-weight:700;margin-bottom:8px;">첫 번째 테스트를 실행해 보세요!</h3>
          <p style="color:var(--text-dim);font-size:13px;margin-bottom:24px;">URL을 등록하고 파이프라인을 실행하면 테스트가 자동 생성됩니다.</p>
          <div style="display:flex;gap:12px;justify-content:center;">
            <button class="action-btn action-btn-primary" onclick="selectView('single_pipeline')">단일 파이프라인 시작</button>
            <button class="action-btn action-btn-primary" onclick="selectView('parallel_pipeline')" style="background:linear-gradient(135deg,#a78bfa 0%,#6366f1 100%);">병렬 파이프라인 시작</button>
          </div>
        </div>` : '';

  main.innerHTML = `
        <div class="ov-wrap">
          <h2 class="ov-heading">Dashboard</h2>
          ${hasAnyData ? hudHtml : ''}
          ${welcomeHtml}
          ${hasAnyData ? `<div class="ov-main-grid">
            <div class="ov-col">${leftCol}</div>
            <div class="ov-col">${rightCol}</div>
          </div>` : ''}
          ${logHtml}
        </div>`;

  // 로그 탭 이벤트 + 자동 갱신
  const logBox = document.getElementById('ov-log-content');
  let _currentLogFile = _uiState.overviewLogTab || 'run_qa.txt';
  let _logAutoRefresh = null;

  async function loadLog(logName) {
    _currentLogFile = logName;
    _uiState.overviewLogTab = logName;
    try {
      const res = await fetch('/api/run_log', { method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify({log: logName}) });
      const data = await res.json();
      if (data.ok && data.log) {
        const lines = data.log.split('\\n');
        const last50 = lines.slice(-50).join('\\n');
        logBox.textContent = last50 || '(빈 로그)';
      } else { logBox.textContent = '(로그 없음)'; }
    } catch(e) { logBox.textContent = '(로그 로드 실패)'; }
    logBox.scrollTop = logBox.scrollHeight;
  }

  // 저장된 탭 상태 복원
  main.querySelectorAll('.ov-log-tab').forEach(btn => {
    if (btn.dataset.log === _currentLogFile) {
      btn.classList.add('active');
    } else {
      btn.classList.remove('active');
    }
    btn.addEventListener('click', () => {
      main.querySelectorAll('.ov-log-tab').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      loadLog(btn.dataset.log);
    });
  });

  // 새로고침 버튼
  document.getElementById('ov-log-refresh').addEventListener('click', () => loadLog(_currentLogFile));

  // 파이프라인 실행 중이면 5초 자동 갱신
  const isRunning = (psStatus !== 'done' && psStatus !== 'idle') || (bsStatus !== 'done' && bsStatus !== 'idle');
  if (isRunning) {
    _logAutoRefresh = setInterval(() => loadLog(_currentLogFile), 5000);
  }

  loadLog(_currentLogFile);
}
