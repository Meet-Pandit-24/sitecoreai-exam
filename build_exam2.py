import json

with open(r'C:\Projects\SitecoreAI\questions_merged.json', 'r', encoding='utf-8') as f:
    questions = json.load(f)

questions_js = json.dumps(questions, ensure_ascii=False)

html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>SitecoreAI CMS Developer Certification — Exam Simulator</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  :root {
    --bg: #0f1117;
    --card: #1a1d27;
    --card2: #222535;
    --border: #2d3148;
    --accent: #e53935;
    --accent2: #ff6659;
    --text: #e8eaf6;
    --muted: #8f9bb3;
    --correct: #00c853;
    --wrong: #f44336;
    --flagged: #ffa000;
    --answered: #3949ab;
    --radius: 10px;
  }
  body { font-family: 'Segoe UI', system-ui, sans-serif; background: var(--bg); color: var(--text); min-height: 100vh; }

  /* ── WELCOME ── */
  #welcome { display:flex; flex-direction:column; align-items:center; justify-content:center; min-height:100vh; padding:24px; text-align:center; }
  #welcome .logo { font-size:52px; margin-bottom:16px; }
  #welcome h1 { font-size:26px; font-weight:700; color:#fff; margin-bottom:6px; }
  #welcome .subtitle { color:var(--muted); font-size:14px; margin-bottom:28px; }
  .info-grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(130px,1fr)); gap:14px; max-width:660px; width:100%; margin-bottom:28px; }
  .info-card { background:var(--card); border:1px solid var(--border); border-radius:var(--radius); padding:18px 14px; }
  .info-card .val { font-size:26px; font-weight:700; color:var(--accent2); }
  .info-card .lbl { font-size:11px; color:var(--muted); margin-top:4px; }
  .section-title { font-size:12px; color:var(--muted); margin-bottom:10px; text-transform:uppercase; letter-spacing:.5px; }
  .mode-row { display:flex; gap:10px; margin-bottom:20px; flex-wrap:wrap; justify-content:center; }
  .mode-btn { padding:9px 18px; border-radius:8px; border:2px solid var(--border); background:var(--card); color:var(--text); cursor:pointer; font-size:13px; transition:all .2s; }
  .mode-btn.active { border-color:var(--accent); background:#2a1a1a; color:#fff; }
  .start-btn { padding:14px 48px; background:var(--accent); color:#fff; border:none; border-radius:var(--radius); font-size:17px; font-weight:700; cursor:pointer; transition:background .2s; }
  .start-btn:hover { background:var(--accent2); }
  .badge-new { font-size:10px; background:#1a3a1a; color:#81c784; border:1px solid #2d5a2d; border-radius:4px; padding:1px 6px; margin-left:6px; vertical-align:middle; }

  /* ── EXAM LAYOUT ── */
  #exam { display:none; height:100vh; flex-direction:column; }
  #exam.active { display:flex; }

  .topbar { background:var(--card); border-bottom:1px solid var(--border); padding:10px 24px; display:flex; align-items:center; justify-content:space-between; flex-shrink:0; gap:12px; }
  .topbar-left { display:flex; align-items:center; gap:14px; }
  .topbar-title { font-size:13px; font-weight:600; color:var(--muted); }
  .timer { font-size:20px; font-weight:700; color:var(--text); font-variant-numeric:tabular-nums; min-width:70px; }
  .timer.warn { color:var(--flagged); animation:pulse 1s infinite; }
  .timer.urgent { color:var(--wrong); animation:pulse .5s infinite; }
  @keyframes pulse { 0%,100%{opacity:1} 50%{opacity:.4} }
  .submit-top { padding:8px 20px; background:var(--accent); color:#fff; border:none; border-radius:8px; cursor:pointer; font-size:13px; font-weight:600; white-space:nowrap; }
  .submit-top:hover { background:var(--accent2); }

  .progress-bar-wrap { height:3px; background:var(--card2); flex-shrink:0; }
  .progress-bar { height:3px; background:linear-gradient(90deg,var(--accent),var(--accent2)); transition:width .3s; }

  .exam-body { display:flex; flex:1; overflow:hidden; }

  .sidebar { width:210px; background:var(--card); border-right:1px solid var(--border); display:flex; flex-direction:column; flex-shrink:0; overflow-y:auto; }
  .sidebar-header { padding:12px 14px; font-size:11px; font-weight:600; color:var(--muted); text-transform:uppercase; letter-spacing:.6px; border-bottom:1px solid var(--border); }
  .q-grid { padding:10px; display:grid; grid-template-columns:repeat(5,1fr); gap:5px; }
  .q-dot { aspect-ratio:1; display:flex; align-items:center; justify-content:center; border-radius:5px; font-size:11px; font-weight:600; cursor:pointer; background:var(--card2); color:var(--muted); border:1px solid var(--border); transition:all .15s; }
  .q-dot:hover { border-color:var(--accent); color:#fff; }
  .q-dot.current { border-color:var(--accent); background:var(--accent); color:#fff; }
  .q-dot.answered { background:var(--answered); color:#fff; border-color:var(--answered); }
  .q-dot.flagged { background:var(--flagged); color:#000; border-color:var(--flagged); }
  .q-dot.answered.flagged { background:var(--flagged); }
  .q-dot.v3new { outline:1px solid #81c784; outline-offset:1px; }
  .sidebar-legend { padding:10px 14px; border-top:1px solid var(--border); font-size:10px; color:var(--muted); display:flex; flex-direction:column; gap:5px; margin-top:auto; }
  .legend-item { display:flex; align-items:center; gap:7px; }
  .legend-dot { width:12px; height:12px; border-radius:3px; flex-shrink:0; }

  .question-panel { flex:1; overflow-y:auto; padding:28px 32px; max-width:820px; margin:0 auto; width:100%; }
  .q-meta { display:flex; align-items:center; gap:10px; margin-bottom:18px; flex-wrap:wrap; }
  .q-num { font-size:13px; color:var(--muted); }
  .q-badge { font-size:11px; padding:3px 10px; border-radius:20px; font-weight:600; }
  .q-badge.multi { background:#1a2a4a; color:#64b5f6; }
  .q-badge.single { background:#1a2a1a; color:#81c784; }
  .q-badge.v3only { background:#1a2a1a; color:#a5d6a7; font-size:10px; }
  .flag-btn { margin-left:auto; padding:5px 12px; border-radius:20px; border:1px solid var(--border); background:transparent; color:var(--muted); cursor:pointer; font-size:12px; transition:all .2s; }
  .flag-btn.flagged { border-color:var(--flagged); color:var(--flagged); background:#2a1e00; }
  .question-text { font-size:17px; font-weight:500; line-height:1.65; margin-bottom:24px; color:#fff; }
  .hint { font-size:13px; color:var(--muted); margin-bottom:16px; font-style:italic; background:var(--card2); padding:8px 14px; border-radius:8px; border-left:3px solid var(--accent); }
  .options { display:flex; flex-direction:column; gap:10px; }
  .option { display:flex; align-items:flex-start; gap:14px; padding:14px 18px; border-radius:var(--radius); border:2px solid var(--border); background:var(--card2); cursor:pointer; transition:all .2s; }
  .option:hover { border-color:#4a5080; background:#1e2238; }
  .option.selected { border-color:var(--accent); background:#2a1a1a; }
  .option.selected .option-key { background:var(--accent); color:#fff; border-color:var(--accent); }
  .option-key { width:30px; height:30px; border-radius:50%; border:2px solid var(--border); display:flex; align-items:center; justify-content:center; font-size:13px; font-weight:700; flex-shrink:0; transition:all .2s; color:var(--muted); }
  .option-text { font-size:15px; line-height:1.5; padding-top:3px; }
  .option.correct-answer { border-color:var(--correct); background:#0d2a1a; }
  .option.correct-answer .option-key { background:var(--correct); color:#fff; border-color:var(--correct); }
  .option.wrong-selected { border-color:var(--wrong); background:#2a0d0d; }
  .option.wrong-selected .option-key { background:var(--wrong); color:#fff; border-color:var(--wrong); }
  .explanation { margin-top:20px; padding:14px 18px; border-radius:var(--radius); border-left:4px solid var(--correct); background:#0a1f12; font-size:14px; line-height:1.6; color:#a5d6a7; }
  .explanation.wrong { border-color:var(--wrong); background:#1a0a0a; color:#ef9a9a; }
  .nav-row { display:flex; justify-content:space-between; align-items:center; margin-top:28px; padding-bottom:28px; }
  .nav-btn { padding:10px 22px; border-radius:8px; border:1px solid var(--border); background:var(--card2); color:var(--text); cursor:pointer; font-size:14px; transition:all .2s; }
  .nav-btn:hover { border-color:var(--accent); color:#fff; }
  .nav-btn:disabled { opacity:.4; cursor:not-allowed; }
  .nav-next { background:var(--accent); border-color:var(--accent); color:#fff; font-weight:600; }
  .nav-next:hover { background:var(--accent2); border-color:var(--accent2); }

  /* ── RESULTS ── */
  #results { display:none; padding:40px 24px; max-width:960px; margin:0 auto; }
  #results.active { display:block; }
  .result-hero { text-align:center; padding:36px; background:var(--card); border:1px solid var(--border); border-radius:16px; margin-bottom:28px; }
  .result-icon { font-size:60px; margin-bottom:14px; }
  .result-score { font-size:72px; font-weight:800; line-height:1; margin-bottom:8px; }
  .result-score.pass { color:var(--correct); }
  .result-score.fail { color:var(--wrong); }
  .result-label { font-size:19px; font-weight:600; margin-bottom:22px; }
  .result-stats { display:grid; grid-template-columns:repeat(auto-fit,minmax(110px,1fr)); gap:14px; max-width:580px; margin:0 auto; }
  .stat-card { background:var(--card2); border-radius:10px; padding:14px; text-align:center; }
  .stat-val { font-size:26px; font-weight:700; }
  .stat-lbl { font-size:11px; color:var(--muted); margin-top:4px; }
  .result-actions { display:flex; gap:10px; justify-content:center; margin-top:22px; flex-wrap:wrap; }
  .result-btn { padding:11px 24px; border-radius:10px; border:1px solid var(--border); background:var(--card2); color:var(--text); cursor:pointer; font-size:13px; font-weight:600; transition:all .2s; }
  .result-btn.primary { background:var(--accent); border-color:var(--accent); color:#fff; }
  .result-btn:hover { opacity:.85; }
  .breakdown-title { font-size:17px; font-weight:600; margin-bottom:14px; }
  .breakdown-list { display:flex; flex-direction:column; gap:8px; }
  .bk-item { background:var(--card); border:1px solid var(--border); border-radius:var(--radius); padding:12px 16px; display:flex; align-items:center; gap:10px; cursor:pointer; transition:background .2s; }
  .bk-item:hover { background:var(--card2); }
  .bk-status { width:26px; height:26px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:13px; flex-shrink:0; }
  .bk-status.ok { background:#0d2a1a; color:var(--correct); }
  .bk-status.fail { background:#2a0d0d; color:var(--wrong); }
  .bk-status.skip { background:var(--card2); color:var(--muted); }
  .bk-q { font-size:12px; color:var(--muted); width:38px; flex-shrink:0; }
  .bk-text { font-size:13px; flex:1; line-height:1.4; }
  .bk-ans { font-size:11px; color:var(--muted); flex-shrink:0; }
  .filter-row { display:flex; gap:8px; margin-bottom:14px; flex-wrap:wrap; }
  .filter-btn { padding:6px 14px; border-radius:20px; border:1px solid var(--border); background:var(--card); color:var(--muted); cursor:pointer; font-size:12px; transition:all .2s; }
  .filter-btn.active { border-color:var(--accent); color:#fff; background:#2a1a1a; }

  .overlay { display:none; position:fixed; inset:0; background:rgba(0,0,0,.75); z-index:100; align-items:center; justify-content:center; }
  .overlay.show { display:flex; }
  .dialog { background:var(--card); border:1px solid var(--border); border-radius:16px; padding:30px; max-width:400px; width:90%; text-align:center; }
  .dialog h3 { font-size:19px; margin-bottom:10px; }
  .dialog p { color:var(--muted); font-size:13px; margin-bottom:22px; line-height:1.5; }
  .dialog-btns { display:flex; gap:10px; justify-content:center; }
  .dialog-btn { padding:10px 26px; border-radius:8px; cursor:pointer; font-size:14px; font-weight:600; border:1px solid var(--border); background:var(--card2); color:var(--text); }
  .dialog-btn.danger { background:var(--accent); border-color:var(--accent); color:#fff; }

  @media(max-width:640px) {
    .sidebar { display:none; }
    .question-panel { padding:16px; }
    .topbar { padding:10px 14px; }
    .topbar-title { display:none; }
  }
</style>
</head>
<body>

<div id="welcome">
  <div class="logo">🎓</div>
  <h1>SitecoreAI CMS Developer Certification</h1>
  <p class="subtitle">Combined Question Bank — V3 + V4 Final &nbsp;|&nbsp; Verified Against Official Sitecore Docs</p>

  <div class="info-grid">
    <div class="info-card"><div class="val">283</div><div class="lbl">Total Questions</div></div>
    <div class="info-card"><div class="val">177</div><div class="lbl">V4 Questions</div></div>
    <div class="info-card"><div class="val">106</div><div class="lbl">New from V3 <span class="badge-new">+added</span></div></div>
    <div class="info-card"><div class="val">70%</div><div class="lbl">Pass Score</div></div>
    <div class="info-card"><div class="val">90min</div><div class="lbl">Full Exam Time</div></div>
  </div>

  <div class="section-title">Number of questions</div>
  <div class="mode-row" id="qCountRow">
    <button class="mode-btn" onclick="setCount(25)">Quick — 25</button>
    <button class="mode-btn" onclick="setCount(50)">Half — 50</button>
    <button class="mode-btn" onclick="setCount(100)">Standard — 100</button>
    <button class="mode-btn" onclick="setCount(177)">V4 Only — 177</button>
    <button class="mode-btn active" onclick="setCount(283)">Full Bank — 283</button>
  </div>

  <div class="section-title">Mode</div>
  <div class="mode-row" id="modeRow">
    <button class="mode-btn active" onclick="setMode('exam')">Exam Mode</button>
    <button class="mode-btn" onclick="setMode('practice')">Practice Mode (instant feedback)</button>
  </div>

  <div class="section-title">Question source</div>
  <div class="mode-row" id="sourceRow">
    <button class="mode-btn active" onclick="setSource('all')">All Questions</button>
    <button class="mode-btn" onclick="setSource('v4')">V4 Only (verified)</button>
    <button class="mode-btn" onclick="setSource('v3new')">V3 New Only (106)</button>
  </div>

  <button class="start-btn" onclick="startExam()">Start Exam →</button>
  <p style="margin-top:16px;font-size:12px;color:var(--muted);">Tip: Use ← → arrow keys to navigate &nbsp;|&nbsp; 1-5 keys to select options</p>
</div>

<div id="exam">
  <div class="topbar">
    <div class="topbar-left">
      <div class="topbar-title">SitecoreAI CMS Exam Simulator</div>
      <div id="statsBar" style="font-size:12px;color:var(--muted);"></div>
    </div>
    <div class="timer" id="timerDisplay">90:00</div>
    <button class="submit-top" onclick="confirmSubmit()">Submit Exam</button>
  </div>
  <div class="progress-bar-wrap"><div class="progress-bar" id="progressBar" style="width:0%"></div></div>
  <div class="exam-body">
    <div class="sidebar">
      <div class="sidebar-header">Questions (<span id="answeredCount">0</span> answered)</div>
      <div class="q-grid" id="qGrid"></div>
      <div class="sidebar-legend">
        <div class="legend-item"><div class="legend-dot" style="background:var(--card2);border:1px solid var(--border)"></div> Not answered</div>
        <div class="legend-item"><div class="legend-dot" style="background:var(--answered)"></div> Answered</div>
        <div class="legend-item"><div class="legend-dot" style="background:var(--flagged)"></div> Flagged</div>
        <div class="legend-item"><div class="legend-dot" style="background:var(--card2);outline:1px solid #81c784;outline-offset:1px"></div> New (V3)</div>
      </div>
    </div>
    <div class="question-panel" id="questionPanel"></div>
  </div>
</div>

<div id="results"></div>

<div class="overlay" id="overlay">
  <div class="dialog">
    <h3>Submit Exam?</h3>
    <p id="dialogMsg">Are you sure you want to submit?</p>
    <div class="dialog-btns">
      <button class="dialog-btn" onclick="closeDialog()">Review</button>
      <button class="dialog-btn danger" onclick="submitExam()">Submit</button>
    </div>
  </div>
</div>

<script>
const ALL_QUESTIONS = """ + questions_js + """;

let examQuestions = [];
let userAnswers = [];
let flagged = [];
let current = 0;
let timerInterval = null;
let timeLeft = 90 * 60;
let mode = 'exam';
let examCount = 283;
let sourceFilter = 'all';
let examStarted = false;
let _details = [];

function setMode(m) {
  mode = m;
  document.querySelectorAll('#modeRow .mode-btn').forEach(b => {
    b.classList.toggle('active', (m === 'exam' && b.textContent.includes('Exam')) || (m === 'practice' && b.textContent.includes('Practice')));
  });
}

function setCount(n) {
  examCount = n;
  document.querySelectorAll('#qCountRow .mode-btn').forEach(b => b.classList.remove('active'));
  event.target.classList.add('active');
}

function setSource(s) {
  sourceFilter = s;
  document.querySelectorAll('#sourceRow .mode-btn').forEach(b => b.classList.remove('active'));
  event.target.classList.add('active');
}

function shuffle(arr) {
  for (let i = arr.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [arr[i], arr[j]] = [arr[j], arr[i]];
  }
  return arr;
}

function startExam() {
  let pool = [...ALL_QUESTIONS];
  if (sourceFilter === 'v4') pool = pool.filter(q => !q.source);
  else if (sourceFilter === 'v3new') pool = pool.filter(q => q.source === 'V3');
  pool = shuffle(pool).slice(0, examCount);
  examQuestions = pool;
  userAnswers = pool.map(() => new Set());
  flagged = pool.map(() => false);
  current = 0;

  document.getElementById('welcome').style.display = 'none';
  document.getElementById('exam').classList.add('active');
  document.getElementById('exam').style.display = 'flex';
  buildGrid();
  renderQuestion();
  startTimer();
  examStarted = true;
}

function startTimer() {
  const mins = examCount <= 25 ? 25 : examCount <= 50 ? 50 : examCount <= 100 ? 70 : examCount <= 177 ? 90 : 150;
  timeLeft = mins * 60;
  updateTimerDisplay();
  timerInterval = setInterval(() => {
    timeLeft--;
    updateTimerDisplay();
    if (timeLeft <= 0) { clearInterval(timerInterval); submitExam(); }
  }, 1000);
}

function updateTimerDisplay() {
  const m = String(Math.floor(timeLeft / 60)).padStart(2, '0');
  const s = String(timeLeft % 60).padStart(2, '0');
  const el = document.getElementById('timerDisplay');
  el.textContent = m + ':' + s;
  el.className = 'timer' + (timeLeft < 300 ? ' urgent' : timeLeft < 600 ? ' warn' : '');
}

function buildGrid() {
  const grid = document.getElementById('qGrid');
  grid.innerHTML = '';
  examQuestions.forEach((q, i) => {
    const d = document.createElement('div');
    d.className = 'q-dot' + (q.source === 'V3' ? ' v3new' : '');
    d.textContent = i + 1;
    d.title = 'Q' + q.id + (q.source ? ' (V3 new)' : '');
    d.onclick = () => goTo(i);
    d.id = 'dot-' + i;
    grid.appendChild(d);
  });
}

function updateGrid() {
  const answeredCount = userAnswers.filter(s => s.size > 0).length;
  document.getElementById('answeredCount').textContent = answeredCount;
  examQuestions.forEach((q, i) => {
    const d = document.getElementById('dot-' + i);
    if (!d) return;
    d.className = 'q-dot' + (q.source === 'V3' ? ' v3new' : '');
    if (i === current) d.classList.add('current');
    if (userAnswers[i].size > 0) d.classList.add('answered');
    if (flagged[i]) d.classList.add('flagged');
  });
  const pct = (answeredCount / examQuestions.length) * 100;
  document.getElementById('progressBar').style.width = pct + '%';
  const statsBar = document.getElementById('statsBar');
  statsBar.textContent = answeredCount + '/' + examQuestions.length + ' answered';
}

function renderQuestion() {
  const q = examQuestions[current];
  const ans = userAnswers[current];
  const isFlagged = flagged[current];
  const showReview = mode === 'practice' && ans.size > 0;
  const correctKeys = q.options.filter(o => o.correct).map(o => o.key);

  const optionsHTML = q.options.map(opt => {
    let cls = 'option';
    if (ans.has(opt.key)) cls += ' selected';
    if (showReview) {
      if (opt.correct) cls = 'option correct-answer';
      else if (ans.has(opt.key)) cls = 'option wrong-selected';
    }
    return `<div class="${cls}" onclick="toggleOption('${opt.key}')" data-key="${opt.key}">
      <div class="option-key">${opt.key}</div>
      <div class="option-text">${escHtml(opt.text)}</div>
    </div>`;
  }).join('');

  let explanationHTML = '';
  if (showReview) {
    const isCorrect = [...ans].sort().join(',') === correctKeys.sort().join(',');
    explanationHTML = `<div class="explanation ${isCorrect ? '' : 'wrong'}">
      ${isCorrect ? '✓ Correct!' : '✗ Incorrect.'}
      &nbsp; Correct answer: <strong>${correctKeys.join(', ')}</strong>
    </div>`;
  }

  const sourceTag = q.source ? '<span class="q-badge v3only">V3 New</span>' : '';

  document.getElementById('questionPanel').innerHTML = `
    <div class="q-meta">
      <span class="q-num">Question ${current + 1} / ${examQuestions.length}</span>
      <span class="q-badge ${q.multi ? 'multi' : 'single'}">${q.multi ? 'Multiple Select' : 'Single Select'}</span>
      ${sourceTag}
      <button class="flag-btn ${isFlagged ? 'flagged' : ''}" onclick="toggleFlag()">
        ${isFlagged ? '🚩 Flagged' : '⚑ Flag'}
      </button>
    </div>
    <div class="question-text">${escHtml(q.question)}</div>
    ${q.multi ? '<div class="hint">Select all correct answers (multiple correct).</div>' : ''}
    <div class="options">${optionsHTML}</div>
    ${explanationHTML}
    <div class="nav-row">
      <button class="nav-btn" onclick="goTo(${current - 1})" ${current === 0 ? 'disabled' : ''}>← Previous</button>
      <button class="nav-btn nav-next" onclick="goTo(${current + 1})" ${current === examQuestions.length - 1 ? 'disabled' : ''}>Next →</button>
    </div>
  `;
  updateGrid();
  document.getElementById('questionPanel').scrollTop = 0;
}

function escHtml(s) {
  return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}

function toggleOption(key) {
  if (mode === 'practice' && userAnswers[current].size > 0) return;
  const q = examQuestions[current];
  const ans = userAnswers[current];
  if (q.multi) {
    if (ans.has(key)) ans.delete(key); else ans.add(key);
  } else {
    ans.clear(); ans.add(key);
  }
  renderQuestion();
}

function toggleFlag() {
  flagged[current] = !flagged[current];
  renderQuestion();
}

function goTo(i) {
  if (i < 0 || i >= examQuestions.length) return;
  current = i;
  renderQuestion();
}

function confirmSubmit() {
  const unanswered = userAnswers.filter(s => s.size === 0).length;
  document.getElementById('dialogMsg').textContent = unanswered > 0
    ? `You have ${unanswered} unanswered question(s). Submit anyway?`
    : 'All questions answered. Ready to submit?';
  document.getElementById('overlay').classList.add('show');
}

function closeDialog() {
  document.getElementById('overlay').classList.remove('show');
}

function submitExam() {
  closeDialog();
  clearInterval(timerInterval);
  showResults();
}

function showResults() {
  document.getElementById('exam').style.display = 'none';
  const resultsEl = document.getElementById('results');
  resultsEl.classList.add('active');

  let correct = 0, wrong = 0, skipped = 0;
  _details = examQuestions.map((q, i) => {
    const ans = userAnswers[i];
    const correctKeys = q.options.filter(o => o.correct).map(o => o.key).sort();
    const userKeys = [...ans].sort();
    if (ans.size === 0) { skipped++; return { q, i, status: 'skip', userKeys, correctKeys }; }
    const isOk = userKeys.join(',') === correctKeys.join(',');
    if (isOk) correct++; else wrong++;
    return { q, i, status: isOk ? 'ok' : 'fail', userKeys, correctKeys };
  });

  const total = examQuestions.length;
  const pct = Math.round((correct / total) * 100);
  const passed = pct >= 70;

  const totalMins = examCount <= 25 ? 25 : examCount <= 50 ? 50 : examCount <= 100 ? 70 : examCount <= 177 ? 90 : 150;
  const timeUsed = totalMins * 60 - timeLeft;
  const min = Math.floor(timeUsed / 60);
  const sec = timeUsed % 60;

  // Category breakdown
  const wrongItems = _details.filter(d => d.status !== 'ok');

  resultsEl.innerHTML = `
    <div class="result-hero">
      <div class="result-icon">${passed ? '🏆' : '📚'}</div>
      <div class="result-score ${passed ? 'pass' : 'fail'}">${pct}%</div>
      <div class="result-label">${passed ? 'PASSED — Well done!' : 'NOT PASSED — Keep going!'}</div>
      <div class="result-stats">
        <div class="stat-card"><div class="stat-val" style="color:var(--correct)">${correct}</div><div class="stat-lbl">Correct</div></div>
        <div class="stat-card"><div class="stat-val" style="color:var(--wrong)">${wrong}</div><div class="stat-lbl">Wrong</div></div>
        <div class="stat-card"><div class="stat-val" style="color:var(--muted)">${skipped}</div><div class="stat-lbl">Skipped</div></div>
        <div class="stat-card"><div class="stat-val">${total}</div><div class="stat-lbl">Total</div></div>
        <div class="stat-card"><div class="stat-val">${min}m ${String(sec).padStart(2,'0')}s</div><div class="stat-lbl">Time Used</div></div>
      </div>
      <div class="result-actions">
        <button class="result-btn primary" onclick="retakeExam()">Retake Exam</button>
        <button class="result-btn" onclick="reviewMode('all')">Review All</button>
        <button class="result-btn" onclick="reviewMode('wrong')">Review Wrong (${wrong + skipped})</button>
      </div>
    </div>
    <div class="filter-row">
      <span style="font-size:13px;color:var(--muted);align-self:center;">Filter:</span>
      <button class="filter-btn active" onclick="filterBreakdown('all',this)">All (${total})</button>
      <button class="filter-btn" onclick="filterBreakdown('ok',this)">Correct (${correct})</button>
      <button class="filter-btn" onclick="filterBreakdown('fail',this)">Wrong (${wrong})</button>
      <button class="filter-btn" onclick="filterBreakdown('skip',this)">Skipped (${skipped})</button>
    </div>
    <div class="breakdown-title">Question Breakdown</div>
    <div class="breakdown-list" id="breakdownList"></div>
  `;

  renderBreakdown('all');
}

function renderBreakdown(filter) {
  const items = filter === 'all' ? _details : _details.filter(d => d.status === filter);
  const html = items.map(d => {
    const icon = d.status === 'ok' ? '✓' : d.status === 'fail' ? '✗' : '–';
    const yourAns = d.userKeys.length ? d.userKeys.join(', ') : 'Skipped';
    const v3tag = d.q.source ? ' <span style="font-size:10px;color:#81c784">[V3]</span>' : '';
    return `<div class="bk-item" onclick="reviewAt(${d.i})">
      <div class="bk-status ${d.status}">${icon}</div>
      <div class="bk-q">Q${d.q.id}</div>
      <div class="bk-text">${escHtml(d.q.question.substring(0, 85))}${d.q.question.length > 85 ? '…' : ''}${v3tag}</div>
      <div class="bk-ans">Your: ${yourAns} | Ans: ${d.correctKeys.join(', ')}</div>
    </div>`;
  }).join('') || '<div style="padding:20px;color:var(--muted);text-align:center">No questions in this filter.</div>';
  document.getElementById('breakdownList').innerHTML = html;
}

function filterBreakdown(filter, btn) {
  document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  renderBreakdown(filter);
}

function retakeExam() {
  document.getElementById('results').classList.remove('active');
  document.getElementById('results').innerHTML = '';
  document.getElementById('welcome').style.display = 'flex';
  examStarted = false;
}

function reviewMode(which) {
  const items = which === 'wrong' ? _details.filter(d => d.status !== 'ok') : _details;
  if (!items.length) { alert('Nothing to review!'); return; }
  examQuestions = items.map(d => d.q);
  userAnswers = items.map(d => new Set(d.userKeys));
  flagged = items.map(() => false);
  current = 0;
  mode = 'practice';
  document.getElementById('results').classList.remove('active');
  document.getElementById('results').innerHTML = '';
  document.getElementById('exam').style.display = 'flex';
  buildGrid();
  renderQuestion();
}

function reviewAt(idx) {
  examQuestions = _details.map(d => d.q);
  userAnswers = _details.map(d => new Set(d.userKeys));
  flagged = _details.map(() => false);
  current = idx;
  mode = 'practice';
  document.getElementById('results').classList.remove('active');
  document.getElementById('results').innerHTML = '';
  document.getElementById('exam').style.display = 'flex';
  buildGrid();
  renderQuestion();
}

function escHtml(s) {
  return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}

document.addEventListener('keydown', e => {
  if (!examStarted) return;
  if (document.getElementById('overlay').classList.contains('show')) return;
  if (e.key === 'ArrowRight' || e.key === 'PageDown') goTo(current + 1);
  if (e.key === 'ArrowLeft' || e.key === 'PageUp') goTo(current - 1);
  if (e.key >= '1' && e.key <= '5') {
    const idx = parseInt(e.key) - 1;
    const opts = examQuestions[current].options;
    if (idx < opts.length) toggleOption(opts[idx].key);
  }
  if (e.key === 'f' || e.key === 'F') toggleFlag();
});
</script>
</body>
</html>"""

with open(r'C:\Projects\SitecoreAI\exam.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f"exam.html rebuilt — {len(html):,} bytes")
print(f"Total questions embedded: {len(questions)}")
v3_new = sum(1 for q in questions if q.get('source') == 'V3')
print(f"  V4 base: {len(questions) - v3_new}")
print(f"  V3 new:  {v3_new}")
