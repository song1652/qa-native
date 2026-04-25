// ── Constants ──
var ROLE_LABEL = { senior: '사수', junior: '부사수', deliberation: '심의' };
var ROLE_CLASS = { senior: 'role-senior', junior: 'role-junior', deliberation: 'role-deliberation' };
var BUBBLE_CLASS = { senior: 'bubble-senior', junior: 'bubble-junior', deliberation: 'bubble-deliberation' };
var STATUS_LABEL = {
  in_progress: '진행 중', discussed: '결론 도출', approved: '승인됨',
  revision_needed: '수정 요청', rejected: '반려됨',
};
var STATUS_CLASS = {
  in_progress: 'status-in_progress', discussed: 'status-in_progress',
  approved: 'status-approved', revision_needed: 'status-revision_needed', rejected: 'status-revision_needed',
};
var MSG_STATUS_STYLE = {
  approved: 'background:#1a2e1e;color:#3fb950;border:1px solid #238636',
  revision_needed: 'background:#2d1212;color:#f85149;border:1px solid #da3633',
};

var PIPELINE_STEPS = ['init', 'analyzed', 'planned', 'generated', 'reviewed', 'done'];
var STEP_LABELS = { init: 'Init', analyzed: '분석', planned: '계획', generated: '생성', reviewed: '리뷰', done: '완료', heal_needed: '힐링필요', heal_failed: '힐링실패', scaffolded: '생성', linted: '생성', approved: '리뷰' };

var PARALLEL_STEPS = ['init', 'analyzing', 'ready', 'generating', 'testing', 'done'];
var PARALLEL_STEP_LABELS = { init: '초기화', analyzing: 'DOM 분석', ready: '코드 생성 대기', generating: '코드 생성', testing: '테스트 실행', done: '완료', heal_needed: '힐링필요', heal_failed: '힐링실패' };

var TESTS_PER_PAGE = 20;
var REPORTS_PER_PAGE = 20;
