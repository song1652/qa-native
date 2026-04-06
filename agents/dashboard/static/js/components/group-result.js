// ── Group Result: 접기/펼치기 공통 ──
function toggleGroupResult(prefix, groupName) {
  const key = prefix + '__' + groupName;
  _groupOpenState[key] = !_groupOpenState[key];
  const body = document.getElementById('grb_' + prefix + '_' + groupName);
  const chv = document.getElementById('grchv_' + prefix + '_' + groupName);
  if (body) body.style.display = _groupOpenState[key] ? 'block' : 'none';
  if (chv) chv.classList.toggle('open', !!_groupOpenState[key]);
}

function buildGroupResultsHtml(gr, prefix) {
  const grNames = Object.keys(gr).sort();
  if (!grNames.length) return '';
  let html = '<div class="group-result-list">';
  grNames.forEach(g => {
    const gd = gr[g];
    const gPass = gd.failed === 0;
    const gCls = gPass ? 'pass' : 'fail';
    const gBadge = gPass ? 'PASS' : 'FAIL';
    const key = prefix + '__' + g;
    const isOpen = !!_groupOpenState[key];
    const testListHtml = buildTestListHtml(gd.tests || [], prefix, g);
    html += `
      <div class="group-result-item">
        <div class="group-result-header" onclick="toggleGroupResult('${esc(prefix)}','${esc(g)}')">
          <span class="group-result-chevron ${isOpen ? 'open' : ''}" id="grchv_${esc(prefix)}_${esc(g)}">&#9654;</span>
          <span class="group-result-dot ${gCls}"></span>
          <span class="group-result-name">${esc(g.replace(/_/g, ' ').toUpperCase())}</span>
          <span class="group-result-count">${gd.passed}/${gd.passed + gd.failed} passed</span>
          <span class="group-result-badge ${gCls}">${gBadge}</span>
        </div>
        <div class="group-result-body" id="grb_${esc(prefix)}_${esc(g)}" style="display:${isOpen ? 'block' : 'none'}">
          ${testListHtml}
        </div>
      </div>`;
  });
  html += '</div>';
  return html;
}
