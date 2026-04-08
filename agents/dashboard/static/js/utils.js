// ── Utility Functions ──
function esc(s) {
  return String(s || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

function fmtTime(iso) {
  if (!iso) return '';
  try { return new Date(iso).toLocaleTimeString('ko-KR', { hour12: false }); } catch { return ''; }
}

function fmtDate(iso) {
  if (!iso) return '';
  try {
    const d = new Date(iso);
    return d.toLocaleDateString('ko-KR') + ' ' + d.toLocaleTimeString('ko-KR', { hour12: false });
  } catch { return ''; }
}

function showToast(msg, type = 'error') {
  const container = document.getElementById('toast-container');
  const el = document.createElement('div');
  el.className = 'toast toast-' + type;
  el.textContent = msg;
  container.appendChild(el);
  setTimeout(() => { if (el.parentNode) el.remove(); }, 3600);
}

function toggleLogExpand(logAreaId) {
  const area = document.getElementById(logAreaId);
  if (!area) return;
  area.classList.toggle('expanded');
  const btn = area.parentElement.querySelector('.log-toggle-btn');
  if (btn) btn.textContent = area.classList.contains('expanded') ? '축소' : '확대';
}

function showHookAlert(type, detail) {
  const existing = document.getElementById('hook-alert');
  if (existing) existing.remove();

  const configs = {
    discuss: {
      icon: '&#x1F4AC;',
      title: '토론이 예약되었습니다',
      desc: `<strong style="color:#89b4fa;">"${esc(detail)}"</strong>`,
      action: 'Claude Code에서 <strong>아무 메시지</strong>를 보내주세요.<br>훅이 자동으로 토론을 시작합니다.'
    },
    parallel: {
      icon: '&#x1F680;',
      title: '병렬 실행 준비 완료',
      desc: `<strong style="color:#89b4fa;">${detail}</strong>`,
      action: 'Claude Code에서 <strong>아무 메시지</strong>를 보내주세요.<br>자동으로 subagent 실행이 시작됩니다.'
    },
    single_init: {
      icon: '&#x2699;&#xFE0F;',
      title: '단일 파이프라인 준비 완료',
      desc: `<strong style="color:#89b4fa;">${detail}</strong>`,
      action: 'Claude Code에서 <strong>아무 메시지</strong>를 보내주세요.<br>훅이 자동으로 파이프라인을 시작합니다.'
    },
    single_approved: {
      icon: '&#x2705;',
      title: '파이프라인 승인 완료',
      desc: `<strong style="color:#89b4fa;">${detail}</strong>`,
      action: 'Claude Code에서 <strong>아무 메시지</strong>를 보내주세요.<br>훅이 자동으로 테스트를 실행합니다.'
    },
    discuss_approved: {
      icon: '&#x1F4DD;',
      title: '팀 토론 승인 완료',
      desc: `<strong style="color:#89b4fa;">${detail}</strong>`,
      action: 'Claude Code에서 <strong>아무 메시지</strong>를 보내주세요.<br>훅이 승인된 항목을 자동으로 구현합니다.'
    }
  };
  const cfg = configs[type] || configs.discuss;

  const overlay = document.createElement('div');
  overlay.id = 'hook-alert';
  overlay.style.cssText = 'position:fixed;inset:0;background:rgba(0,0,0,0.55);display:flex;align-items:center;justify-content:center;z-index:9999;animation:fadeIn 0.2s ease;';

  const box = document.createElement('div');
  box.style.cssText = 'background:#1e1e2e;border:2px solid #f9e2af;border-radius:16px;padding:32px 40px;max-width:500px;text-align:center;box-shadow:0 20px 60px rgba(0,0,0,0.5);';
  box.innerHTML = `
    <div style="font-size:48px;margin-bottom:16px;">${cfg.icon}</div>
    <h2 style="color:#cdd6f4;margin:0 0 12px;">${cfg.title}</h2>
    <p style="color:#a6adc8;font-size:14px;line-height:1.6;margin:0 0 8px;">${cfg.desc}</p>
    <div style="background:#313244;border-radius:10px;padding:16px 20px;margin:16px 0 24px;">
      <p style="color:#f9e2af;font-size:14px;line-height:1.7;margin:0;">
        ${cfg.action}
      </p>
    </div>
    <button onclick="this.closest('#hook-alert').remove()"
      style="background:#f9e2af;color:#1e1e2e;border:none;border-radius:8px;padding:10px 28px;font-size:14px;font-weight:600;cursor:pointer;">
      확인
    </button>
  `;
  overlay.appendChild(box);
  overlay.addEventListener('click', (e) => { if (e.target === overlay) overlay.remove(); });
  document.body.appendChild(overlay);
}

// 로그 폴링 (3초 간격, 최대 120초)
function startLogPolling(logAreaId, logContentId, logFileName) {
  if (_logTimers[logAreaId]) clearInterval(_logTimers[logAreaId]);
  const area = document.getElementById(logAreaId);
  if (area) area.style.display = 'block';
  // 토글 버튼 표시
  const toggleId = logAreaId === 'run-single-log' ? 'log-toggle-single' : 'log-toggle-parallel';
  const toggleBtn = document.getElementById(toggleId);
  if (toggleBtn) toggleBtn.style.display = 'inline-block';
  let elapsed = 0;
  const poll = async () => {
    try {
      const res = await fetch('/api/run_log', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ log: logFileName }),
      });
      const data = await res.json();
      const el = document.getElementById(logContentId);
      if (el) {
        el.textContent = data.log || '(대기 중...)';
        const logArea = document.getElementById(logAreaId);
        if (logArea) logArea.scrollTop = logArea.scrollHeight;
      }
    } catch (e) { }
    elapsed += 3;
    if (elapsed >= 120 && _logTimers[logAreaId]) {
      clearInterval(_logTimers[logAreaId]);
      delete _logTimers[logAreaId];
    }
  };
  poll();
  _logTimers[logAreaId] = setInterval(poll, 3000);
}
