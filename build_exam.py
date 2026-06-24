import json

with open(r'C:\Projects\SitecoreAI\questions.json', 'r', encoding='utf-8') as f:
    questions = json.load(f)

questions_js = json.dumps(questions, ensure_ascii=False)

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>SitecoreAI CMS Developer Certification — Exam Simulator</title>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  :root {{
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
  }}
  body {{ font-family: 'Segoe UI', system-ui, sans-serif; background: var(--bg); color: var(--text); min-height: 100vh; }}

  /* ── WELCOME SCREEN ── */
  #welcome {{ display:flex; flex-direction:column; align-items:center; justify-content:center; min-height:100vh; padding:24px; text-align:center; }}
  #welcome .logo {{ font-size:48px; margin-bottom:16px; }}
  #welcome h1 {{ font-size:28px; font-weight:700; color:#fff; margin-bottom:8px; }}
  #welcome .subtitle {{ color:var(--muted); font-size:15px; margin-bottom:32px; }}
  .info-grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(140px,1fr)); gap:16px; max-width:640px; width:100%; margin-bottom:32px; }}
  .info-card {{ background:var(--card); border:1px solid var(--border); border-radius:var(--radius); padding:20px 16px; }}
  .info-card .val {{ font-size:28px; font-weight:700; color:var(--accent2); }}
  .info-card .lbl {{ font-size:12px; color:var(--muted); margin-top:4px; }}
  .mode-row {{ display:flex; gap:12px; margin-bottom:24px; flex-wrap:wrap; justify-content:center; }}
  .mode-btn {{ padding:10px 22px; border-radius:8px; border:2px solid var(--border); background:var(--card); color:var(--text); cursor:pointer; font-size:14px; transition:all .2s; }}
  .mode-btn.active {{ border-color:var(--accent); background:#2a1a1a; color:#fff; }}
  .start-btn {{ padding:14px 48px; background:var(--accent); color:#fff; border:none; border-radius:var(--radius); font-size:17px; font-weight:700; cursor:pointer; transition:background .2s; letter-spacing:.3px; }}
  .start-btn:hover {{ background:var(--accent2); }}

  /* ── EXAM LAYOUT ── */
  #exam {{ display:none; height:100vh; display:none; flex-direction:column; }}
  #exam.active {{ display:flex; }}

  /* top bar */
  .topbar {{ background:var(--card); border-bottom:1px solid var(--border); padding:12px 24px; display:flex; align-items:center; justify-content:space-between; flex-shrink:0; }}
  .topbar-title {{ font-size:14px; font-weight:600; color:var(--muted); }}
  .timer {{ font-size:20px; font-weight:700; color:var(--text); font-variant-numeric:tabular-nums; }}
  .timer.warn {{ color:var(--flagged); animation:pulse 1s infinite; }}
  .timer.urgent {{ color:var(--wrong); animation:pulse .5s infinite; }}
  @keyframes pulse {{ 0%,100%{{opacity:1}} 50%{{opacity:.5}} }}
  .submit-top {{ padding:8px 20px; background:var(--accent); color:#fff; border:none; border-radius:8px; cursor:pointer; font-size:14px; font-weight:600; }}

  /* progress */
  .progress-bar-wrap {{ height:4px; background:var(--card2); flex-shrink:0; }}
  .progress-bar {{ height:4px; background:linear-gradient(90deg,var(--accent),var(--accent2)); transition:width .3s; }}

  /* main area */
  .exam-body {{ display:flex; flex:1; overflow:hidden; }}

  /* sidebar */
  .sidebar {{ width:220px; background:var(--card); border-right:1px solid var(--border); display:flex; flex-direction:column; flex-shrink:0; overflow-y:auto; }}
  .sidebar-header {{ padding:14px 16px; font-size:12px; font-weight:600; color:var(--muted); text-transform:uppercase; letter-spacing:.6px; border-bottom:1px solid var(--border); }}
  .q-grid {{ padding:12px; display:grid; grid-template-columns:repeat(5,1fr); gap:6px; }}
  .q-dot {{ aspect-ratio:1; display:flex; align-items:center; justify-content:center; border-radius:6px; font-size:12px; font-weight:600; cursor:pointer; background:var(--card2); color:var(--muted); border:1px solid var(--border); transition:all .15s; }}
  .q-dot:hover {{ border-color:var(--accent); color:#fff; }}
  .q-dot.current {{ border-color:var(--accent); background:var(--accent); color:#fff; }}
  .q-dot.answered {{ background:var(--answered); color:#fff; border-color:var(--answered); }}
  .q-dot.flagged {{ background:var(--flagged); color:#fff; border-color:var(--flagged); }}
  .q-dot.answered.flagged {{ background:var(--flagged); }}
  .sidebar-legend {{ padding:12px 16px; border-top:1px solid var(--border); font-size:11px; color:var(--muted); display:flex; flex-direction:column; gap:6px; margin-top:auto; }}
  .legend-item {{ display:flex; align-items:center; gap:8px; }}
  .legend-dot {{ width:14px; height:14px; border-radius:4px; flex-shrink:0; }}

  /* question panel */
  .question-panel {{ flex:1; overflow-y:auto; padding:32px; max-width:800px; margin:0 auto; width:100%; }}
  .q-meta {{ display:flex; align-items:center; gap:12px; margin-bottom:20px; }}
  .q-num {{ font-size:13px; color:var(--muted); }}
  .q-badge {{ font-size:11px; padding:3px 10px; border-radius:20px; font-weight:600; }}
  .q-badge.multi {{ background:#1a2a4a; color:#64b5f6; }}
  .q-badge.single {{ background:#1a2a1a; color:#81c784; }}
  .flag-btn {{ margin-left:auto; padding:6px 14px; border-radius:20px; border:1px solid var(--border); background:transparent; color:var(--muted); cursor:pointer; font-size:12px; transition:all .2s; }}
  .flag-btn.flagged {{ border-color:var(--flagged); color:var(--flagged); background:#2a1e00; }}
  .question-text {{ font-size:18px; font-weight:500; line-height:1.6; margin-bottom:28px; color:#fff; }}
  .hint {{ font-size:13px; color:var(--muted); margin-bottom:20px; font-style:italic; }}
  .options {{ display:flex; flex-direction:column; gap:12px; }}
  .option {{ display:flex; align-items:flex-start; gap:14px; padding:16px 20px; border-radius:var(--radius); border:2px solid var(--border); background:var(--card2); cursor:pointer; transition:all .2s; }}
  .option:hover {{ border-color:#4a5080; background:#1e2238; }}
  .option.selected {{ border-color:var(--accent); background:#2a1a1a; }}
  .option.selected .opt-key {{ background:var(--accent); color:#fff; border-color:var(--accent); }}
  .option-key {{ width:32px; height:32px; border-radius:50%; border:2px solid var(--border); display:flex; align-items:center; justify-content:center; font-size:13px; font-weight:700; flex-shrink:0; transition:all .2s; color:var(--muted); }}
  .option-text {{ font-size:15px; line-height:1.5; padding-top:4px; }}

  /* review mode states */
  .option.correct-answer {{ border-color:var(--correct); background:#0d2a1a; }}
  .option.correct-answer .option-key {{ background:var(--correct); color:#fff; border-color:var(--correct); }}
  .option.wrong-selected {{ border-color:var(--wrong); background:#2a0d0d; }}
  .option.wrong-selected .option-key {{ background:var(--wrong); color:#fff; border-color:var(--wrong); }}

  .explanation {{ margin-top:24px; padding:16px 20px; border-radius:var(--radius); border-left:4px solid var(--correct); background:#0a1f12; font-size:14px; line-height:1.6; color:#a5d6a7; }}
  .explanation.wrong {{ border-color:var(--wrong); background:#1a0a0a; color:#ef9a9a; }}

  /* nav buttons */
  .nav-row {{ display:flex; justify-content:space-between; align-items:center; margin-top:32px; padding-bottom:32px; }}
  .nav-btn {{ padding:10px 24px; border-radius:8px; border:1px solid var(--border); background:var(--card2); color:var(--text); cursor:pointer; font-size:14px; transition:all .2s; }}
  .nav-btn:hover {{ border-color:var(--accent); color:#fff; }}
  .nav-btn:disabled {{ opacity:.4; cursor:not-allowed; }}
  .nav-next {{ background:var(--accent); border-color:var(--accent); color:#fff; font-weight:600; }}
  .nav-next:hover {{ background:var(--accent2); border-color:var(--accent2); }}

  /* ── RESULTS SCREEN ── */
  #results {{ display:none; padding:40px 24px; max-width:900px; margin:0 auto; }}
  #results.active {{ display:block; }}
  .result-hero {{ text-align:center; padding:40px; background:var(--card); border:1px solid var(--border); border-radius:16px; margin-bottom:32px; }}
  .result-icon {{ font-size:64px; margin-bottom:16px; }}
  .result-score {{ font-size:72px; font-weight:800; line-height:1; margin-bottom:8px; }}
  .result-score.pass {{ color:var(--correct); }}
  .result-score.fail {{ color:var(--wrong); }}
  .result-label {{ font-size:20px; font-weight:600; margin-bottom:24px; }}
  .result-stats {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(120px,1fr)); gap:16px; max-width:600px; margin:0 auto; }}
  .stat-card {{ background:var(--card2); border-radius:10px; padding:16px; text-align:center; }}
  .stat-val {{ font-size:28px; font-weight:700; }}
  .stat-lbl {{ font-size:12px; color:var(--muted); margin-top:4px; }}
  .result-actions {{ display:flex; gap:12px; justify-content:center; margin-top:24px; flex-wrap:wrap; }}
  .result-btn {{ padding:12px 28px; border-radius:10px; border:1px solid var(--border); background:var(--card2); color:var(--text); cursor:pointer; font-size:14px; font-weight:600; transition:all .2s; }}
  .result-btn.primary {{ background:var(--accent); border-color:var(--accent); color:#fff; }}
  .result-btn:hover {{ opacity:.85; }}
  .breakdown-title {{ font-size:18px; font-weight:600; margin-bottom:16px; }}
  .breakdown-list {{ display:flex; flex-direction:column; gap:10px; }}
  .bk-item {{ background:var(--card); border:1px solid var(--border); border-radius:var(--radius); padding:14px 18px; display:flex; align-items:center; gap:12px; cursor:pointer; transition:background .2s; }}
  .bk-item:hover {{ background:var(--card2); }}
  .bk-status {{ width:28px; height:28px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:14px; flex-shrink:0; }}
  .bk-status.ok {{ background:#0d2a1a; color:var(--correct); }}
  .bk-status.fail {{ background:#2a0d0d; color:var(--wrong); }}
  .bk-status.skip {{ background:var(--card2); color:var(--muted); }}
  .bk-q {{ font-size:13px; color:var(--muted); width:40px; flex-shrink:0; }}
  .bk-text {{ font-size:14px; flex:1; line-height:1.4; }}
  .bk-ans {{ font-size:12px; color:var(--muted); flex-shrink:0; }}

  /* Confirm dialog */
  .overlay {{ display:none; position:fixed; inset:0; background:rgba(0,0,0,.7); z-index:100; align-items:center; justify-content:center; }}
  .overlay.show {{ display:flex; }}
  .dialog {{ background:var(--card); border:1px solid var(--border); border-radius:16px; padding:32px; max-width:420px; width:90%; text-align:center; }}
  .dialog h3 {{ font-size:20px; margin-bottom:12px; }}
  .dialog p {{ color:var(--muted); font-size:14px; margin-bottom:24px; line-height:1.5; }}
  .dialog-btns {{ display:flex; gap:12px; justify-content:center; }}
  .dialog-btn {{ padding:10px 28px; border-radius:8px; cursor:pointer; font-size:14px; font-weight:600; border:1px solid var(--border); background:var(--card2); color:var(--text); }}
  .dialog-btn.danger {{ background:var(--accent); border-color:var(--accent); color:#fff; }}

  @media(max-width:640px) {{
    .sidebar {{ display:none; }}
    .question-panel {{ padding:20px 16px; }}
    .topbar {{ padding:10px 16px; }}
  }}
</style>
</head>
<body>

<!-- ══ WELCOME ══ -->
<div id="welcome">
  <div class="logo">🎓</div>
  <h1>SitecoreAI CMS Developer Certification</h1>
  <p class="subtitle">Consolidated Question Bank — V4 Final &nbsp;|&nbsp; 177 Questions</p>

  <div class="info-grid">
    <div class="info-card"><div class="val">177</div><div class="lbl">Total Questions</div></div>
    <div class="info-card"><div class="val">90</div><div class="lbl">Min to Pass (70%)</div></div>
    <div class="info-card"><div class="val">90<span style="font-size:14px">min</span></div><div class="lbl">Time Limit</div></div>
    <div class="info-card"><div class="val">70%</div><div class="lbl">Pass Score</div></div>
  </div>

  <div style="margin-bottom:12px;color:var(--muted);font-size:13px;">Select number of questions:</div>
  <div class="mode-row" id="qCountRow">
    <button class="mode-btn" onclick="setCount(25)">25 Questions</button>
    <button class="mode-btn" onclick="setCount(50)">50 Questions</button>
    <button class="mode-btn" onclick="setCount(100)">100 Questions</button>
    <button class="mode-btn active" onclick="setCount(177)">Full Exam (177)</button>
  </div>
  <div style="margin-bottom:12px;color:var(--muted);font-size:13px;">Mode:</div>
  <div class="mode-row" id="modeRow">
    <button class="mode-btn active" onclick="setMode('exam')">Exam Mode</button>
    <button class="mode-btn" onclick="setMode('practice')">Practice Mode (instant feedback)</button>
  </div>

  <button class="start-btn" onclick="startExam()">Start Exam →</button>
</div>

<!-- ══ EXAM ══ -->
<div id="exam">
  <div class="topbar">
    <div class="topbar-title">SitecoreAI CMS — Exam Simulator</div>
    <div class="timer" id="timerDisplay">90:00</div>
    <button class="submit-top" onclick="confirmSubmit()">Submit Exam</button>
  </div>
  <div class="progress-bar-wrap"><div class="progress-bar" id="progressBar" style="width:0%"></div></div>
  <div class="exam-body">
    <div class="sidebar">
      <div class="sidebar-header">Questions</div>
      <div class="q-grid" id="qGrid"></div>
      <div class="sidebar-legend">
        <div class="legend-item"><div class="legend-dot" style="background:var(--card2);border:1px solid var(--border)"></div>Not visited</div>
        <div class="legend-item"><div class="legend-dot" style="background:var(--answered)"></div>Answered</div>
        <div class="legend-item"><div class="legend-dot" style="background:var(--flagged)"></div>Flagged</div>
      </div>
    </div>
    <div class="question-panel" id="questionPanel"></div>
  </div>
</div>

<!-- ══ RESULTS ══ -->
<div id="results"></div>

<!-- ══ CONFIRM DIALOG ══ -->
<div class="overlay" id="overlay">
  <div class="dialog">
    <h3>Submit Exam?</h3>
    <p id="dialogMsg">Are you sure you want to submit? You can review unanswered questions before submitting.</p>
    <div class="dialog-btns">
      <button class="dialog-btn" onclick="closeDialog()">Review</button>
      <button class="dialog-btn danger" onclick="submitExam()">Submit</button>
    </div>
  </div>
</div>

<script>
const ALL_QUESTIONS = {questions_js};

let examQuestions = [];
let userAnswers = []; // array of Set (selected keys)
let flagged = [];
let current = 0;
let timerInterval = null;
let timeLeft = 90 * 60;
let mode = 'exam';
let examCount = 177;
let examStarted = false;

function setMode(m) {{
  mode = m;
  document.querySelectorAll('#modeRow .mode-btn').forEach(b => b.classList.remove('active'));
  document.querySelectorAll('#modeRow .mode-btn').forEach(b => {{
    if ((m === 'exam' && b.textContent.includes('Exam')) || (m === 'practice' && b.textContent.includes('Practice')))
      b.classList.add('active');
  }});
}}

function setCount(n) {{
  examCount = n;
  document.querySelectorAll('#qCountRow .mode-btn').forEach(b => b.classList.remove('active'));
  event.target.classList.add('active');
}}

function shuffle(arr) {{
  for (let i = arr.length - 1; i > 0; i--) {{
    const j = Math.floor(Math.random() * (i + 1));
    [arr[i], arr[j]] = [arr[j], arr[i]];
  }}
  return arr;
}}

function startExam() {{
  const pool = shuffle([...ALL_QUESTIONS]).slice(0, examCount);
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
}}

function startTimer() {{
  timeLeft = (examCount <= 25 ? 25 : examCount <= 50 ? 50 : examCount <= 100 ? 70 : 90) * 60;
  updateTimerDisplay();
  timerInterval = setInterval(() => {{
    timeLeft--;
    updateTimerDisplay();
    if (timeLeft <= 0) {{ clearInterval(timerInterval); submitExam(); }}
  }}, 1000);
}}

function updateTimerDisplay() {{
  const m = String(Math.floor(timeLeft / 60)).padStart(2, '0');
  const s = String(timeLeft % 60).padStart(2, '0');
  const el = document.getElementById('timerDisplay');
  el.textContent = m + ':' + s;
  el.className = 'timer' + (timeLeft < 300 ? ' urgent' : timeLeft < 600 ? ' warn' : '');
}}

function buildGrid() {{
  const grid = document.getElementById('qGrid');
  grid.innerHTML = '';
  examQuestions.forEach((_, i) => {{
    const d = document.createElement('div');
    d.className = 'q-dot';
    d.textContent = i + 1;
    d.onclick = () => goTo(i);
    d.id = 'dot-' + i;
    grid.appendChild(d);
  }});
}}

function updateGrid() {{
  examQuestions.forEach((_, i) => {{
    const d = document.getElementById('dot-' + i);
    if (!d) return;
    d.className = 'q-dot';
    if (i === current) d.classList.add('current');
    if (userAnswers[i].size > 0) d.classList.add('answered');
    if (flagged[i]) d.classList.add('flagged');
  }});
  const pct = (userAnswers.filter(s => s.size > 0).length / examQuestions.length) * 100;
  document.getElementById('progressBar').style.width = pct + '%';
}}

function renderQuestion() {{
  const q = examQuestions[current];
  const ans = userAnswers[current];
  const isFlagged = flagged[current];
  const showReview = mode === 'practice' && ans.size > 0;

  const correctKeys = q.options.filter(o => o.correct).map(o => o.key);

  let optionsHTML = q.options.map(opt => {{
    let cls = 'option';
    let keyCls = 'option-key';
    if (ans.has(opt.key)) cls += ' selected';
    if (showReview) {{
      if (opt.correct) cls = 'option correct-answer';
      else if (ans.has(opt.key)) cls = 'option wrong-selected';
    }}
    return `<div class="${{cls}}" onclick="toggleOption('${{opt.key}}')" data-key="${{opt.key}}">
      <div class="${{keyCls}}">${{opt.key}}</div>
      <div class="option-text">${{escHtml(opt.text)}}</div>
    </div>`;
  }}).join('');

  let explanationHTML = '';
  if (showReview) {{
    const isCorrect = [...ans].sort().join(',') === correctKeys.sort().join(',');
    explanationHTML = `<div class="explanation ${{isCorrect ? '' : 'wrong'}}">
      ${{isCorrect ? '✓ Correct!' : '✗ Incorrect.'}}
      Correct answer: <strong>${{correctKeys.join(', ')}}</strong>
    </div>`;
  }}

  const panel = document.getElementById('questionPanel');
  panel.innerHTML = `
    <div class="q-meta">
      <span class="q-num">Question ${{current + 1}} of ${{examQuestions.length}}</span>
      <span class="q-badge ${{q.multi ? 'multi' : 'single'}}">${{q.multi ? 'Multiple Select' : 'Single Select'}}</span>
      <button class="flag-btn ${{isFlagged ? 'flagged' : ''}}" onclick="toggleFlag()">
        ${{isFlagged ? '🚩 Flagged' : '⚑ Flag for Review'}}
      </button>
    </div>
    <div class="question-text">${{escHtml(q.question)}}</div>
    ${{q.multi ? '<div class="hint">Select all that apply.</div>' : ''}}
    <div class="options" id="optionsContainer">${{optionsHTML}}</div>
    ${{explanationHTML}}
    <div class="nav-row">
      <button class="nav-btn" onclick="goTo(${{current - 1}})" ${{current === 0 ? 'disabled' : ''}}>← Previous</button>
      <button class="nav-btn nav-next" onclick="goTo(${{current + 1}})" ${{current === examQuestions.length - 1 ? 'disabled' : ''}}>Next →</button>
    </div>
  `;
  updateGrid();
  panel.scrollTop = 0;
}}

function escHtml(s) {{
  return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}}

function toggleOption(key) {{
  if (mode === 'practice' && userAnswers[current].size > 0) return; // locked after answer in practice
  const q = examQuestions[current];
  const ans = userAnswers[current];
  if (q.multi) {{
    if (ans.has(key)) ans.delete(key); else ans.add(key);
  }} else {{
    ans.clear();
    ans.add(key);
  }}
  renderQuestion();
}}

function toggleFlag() {{
  flagged[current] = !flagged[current];
  renderQuestion();
}}

function goTo(i) {{
  if (i < 0 || i >= examQuestions.length) return;
  current = i;
  renderQuestion();
}}

function confirmSubmit() {{
  const unanswered = userAnswers.filter(s => s.size === 0).length;
  const msg = unanswered > 0
    ? `You have ${{unanswered}} unanswered question(s). Are you sure you want to submit?`
    : 'All questions answered. Ready to submit?';
  document.getElementById('dialogMsg').textContent = msg;
  document.getElementById('overlay').classList.add('show');
}}

function closeDialog() {{
  document.getElementById('overlay').classList.remove('show');
}}

function submitExam() {{
  closeDialog();
  clearInterval(timerInterval);
  showResults();
}}

function showResults() {{
  document.getElementById('exam').style.display = 'none';
  const resultsEl = document.getElementById('results');
  resultsEl.classList.add('active');

  let correct = 0, wrong = 0, skipped = 0;
  const details = examQuestions.map((q, i) => {{
    const ans = userAnswers[i];
    const correctKeys = q.options.filter(o => o.correct).map(o => o.key).sort();
    const userKeys = [...ans].sort();
    if (ans.size === 0) {{ skipped++; return {{ q, i, status: 'skip', userKeys, correctKeys }}; }}
    const isOk = userKeys.join(',') === correctKeys.join(',');
    if (isOk) correct++; else wrong++;
    return {{ q, i, status: isOk ? 'ok' : 'fail', userKeys, correctKeys }};
  }});

  const total = examQuestions.length;
  const pct = Math.round((correct / total) * 100);
  const passed = pct >= 70;

  const timeUsed = ((examCount <= 25 ? 25 : examCount <= 50 ? 50 : examCount <= 100 ? 70 : 90) * 60) - timeLeft;
  const min = Math.floor(timeUsed / 60);
  const sec = timeUsed % 60;

  const breakdownHTML = details.map(d => {{
    const icon = d.status === 'ok' ? '✓' : d.status === 'fail' ? '✗' : '–';
    const cls = d.status;
    const yourAns = d.userKeys.length ? d.userKeys.join(', ') : 'Not answered';
    return `<div class="bk-item" onclick="reviewQuestion(${{d.i}})">
      <div class="bk-status ${{cls}}">${{icon}}</div>
      <div class="bk-q">Q${{d.q.id}}</div>
      <div class="bk-text">${{escHtml(d.q.question.substring(0, 80))}}${{d.q.question.length > 80 ? '…' : ''}}</div>
      <div class="bk-ans">Your: ${{yourAns}} &nbsp;|&nbsp; Correct: ${{d.correctKeys.join(', ')}}</div>
    </div>`;
  }}).join('');

  resultsEl.innerHTML = `
    <div class="result-hero">
      <div class="result-icon">${{passed ? '🏆' : '📚'}}</div>
      <div class="result-score ${{passed ? 'pass' : 'fail'}}">${{pct}}%</div>
      <div class="result-label">${{passed ? 'PASSED — Congratulations!' : 'NOT PASSED — Keep Studying!'}}</div>
      <div class="result-stats">
        <div class="stat-card"><div class="stat-val" style="color:var(--correct)">${{correct}}</div><div class="stat-lbl">Correct</div></div>
        <div class="stat-card"><div class="stat-val" style="color:var(--wrong)">${{wrong}}</div><div class="stat-lbl">Wrong</div></div>
        <div class="stat-card"><div class="stat-val" style="color:var(--muted)">${{skipped}}</div><div class="stat-lbl">Skipped</div></div>
        <div class="stat-card"><div class="stat-val">${{min}}m ${{String(sec).padStart(2,'0')}}s</div><div class="stat-lbl">Time Used</div></div>
      </div>
      <div class="result-actions">
        <button class="result-btn primary" onclick="retakeExam()">Retake Exam</button>
        <button class="result-btn" onclick="reviewAll()">Review All Questions</button>
        <button class="result-btn" onclick="reviewWrong()">Review Wrong Only (${{wrong + skipped}})</button>
      </div>
    </div>
    <div class="breakdown-title">Question Breakdown (click to review)</div>
    <div class="breakdown-list">${{breakdownHTML}}</div>
  `;

  window._details = details;
}}

function retakeExam() {{
  document.getElementById('results').classList.remove('active');
  document.getElementById('results').innerHTML = '';
  document.getElementById('welcome').style.display = 'flex';
  examStarted = false;
}}

function reviewAll() {{
  enterReviewMode(_details, false);
}}

function reviewWrong() {{
  enterReviewMode(_details.filter(d => d.status !== 'ok'), true);
}}

function enterReviewMode(items, wrongOnly) {{
  if (items.length === 0) {{ alert('No questions to review!'); return; }}
  // Switch back to exam view in review/practice mode
  examQuestions = items.map(d => d.q);
  userAnswers = items.map(d => new Set(d.userKeys));
  flagged = items.map(() => false);
  current = 0;
  mode = 'practice'; // show answers

  document.getElementById('results').classList.remove('active');
  document.getElementById('results').innerHTML = '';
  document.getElementById('exam').style.display = 'flex';
  buildGrid();
  renderQuestion();
}}

function reviewQuestion(idx) {{
  // Go to exam review mode at that question
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
}}

// Keyboard nav
document.addEventListener('keydown', e => {{
  if (!examStarted) return;
  if (e.key === 'ArrowRight') goTo(current + 1);
  if (e.key === 'ArrowLeft') goTo(current - 1);
  if (e.key >= '1' && e.key <= '9') {{
    const idx = parseInt(e.key) - 1;
    if (idx < examQuestions[current].options.length) toggleOption(examQuestions[current].options[idx].key);
  }}
}});
</script>
</body>
</html>"""

with open(r'C:\Projects\SitecoreAI\exam.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('exam.html created')
print(f'Size: {len(html):,} bytes')
