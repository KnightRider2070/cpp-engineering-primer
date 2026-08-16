// =============================================================================
//  The browser half. Course-owned; you never have to write this.
// =============================================================================
//
//  Two things in here are worth noticing when you get to Stage 5.
//
//  1. THE 0-8 / 1-9 THING NEVER BECOMES A CONVERSION.
//     The loop below builds nine buttons with i = 0..8, which is already what
//     your C++ expects, so a click sends `cell: i` untouched. The only place
//     1-9 exists is the LABEL we draw on an empty square. "Humans count from
//     one" turned out to be a presentation detail, not a data problem.
//
//  2. THERE IS ONE render() AND IT TAKES A WHOLE BOARD.
//     Every endpoint returns the complete state, so there is no code here that
//     tries to keep a local copy in sync with the server. That class of bug
//     simply cannot happen. It also means that when you add a computer
//     opponent at Stage 7 -- and a single move suddenly comes back with TWO new
//     marks on the board -- not one line of this file has to change.
// =============================================================================

const boardEl   = document.getElementById('board');
const statusEl  = document.getElementById('status');
const msgEl     = document.getElementById('msg');
const pillEl    = document.getElementById('state-pill');
const histEl    = document.getElementById('history');
const connDot   = document.getElementById('conn-dot');
const connText  = document.getElementById('conn-text');

const WIN_LINES = [
  [0,1,2],[3,4,5],[6,7,8],
  [0,3,6],[1,4,7],[2,5,8],
  [0,4,8],[2,4,6],
];

let history = [];
let previous = null;

// --- build the nine cells once ---------------------------------------------
const cells = [];
for (let i = 0; i < 9; i++) {
  const button = document.createElement('button');
  button.className = 'cell';
  button.dataset.cell = String(i);
  button.setAttribute('aria-label', `cell ${i + 1}`);
  button.addEventListener('click', () => send('/api/move', { cell: i }));
  boardEl.append(button);
  cells.push(button);
}

document.getElementById('new-game').addEventListener('click', () => {
  history = [];
  previous = null;
  send('/api/reset', null);
});

// --- rendering --------------------------------------------------------------
function winningLine(state) {
  if (state.status !== 'won' || !state.winner) return null;
  return WIN_LINES.find(([a, b, c]) =>
    state.board[a] === state.winner &&
    state.board[b] === state.winner &&
    state.board[c] === state.winner) || null;
}

function render(state) {
  if (!state) return;
  const line = winningLine(state);
  const finished = state.status !== 'in_progress';

  cells.forEach((button, i) => {
    const mark = state.board[i];
    const empty = mark === 'empty';
    button.textContent = empty ? String(i + 1) : mark.toUpperCase();
    button.className = 'cell ' + (empty ? 'empty' : mark) +
                       (line && line.includes(i) ? ' win' : '');
    button.disabled = !empty || finished;
  });

  if (state.status === 'won') {
    statusEl.textContent = `${state.winner.toUpperCase()} WINS`;
    pillEl.textContent = 'WON';
    pillEl.className = 'state-pill won';
  } else if (state.status === 'draw') {
    statusEl.textContent = 'DRAW';
    pillEl.textContent = 'DRAW';
    pillEl.className = 'state-pill draw';
  } else {
    statusEl.textContent = `${state.turn.toUpperCase()} to play`;
    pillEl.textContent = 'IN PROGRESS';
    pillEl.className = 'state-pill';
  }

  recordHistory(state);
  renderHistory();
  previous = state;
}

// Work out what changed so the move list stays right even when the computer
// answers instantly and two marks appear at once.
function recordHistory(state) {
  if (!previous) { previous = state; return; }
  for (let i = 0; i < 9; i++) {
    if (previous.board[i] === 'empty' && state.board[i] !== 'empty') {
      history.push({ mark: state.board[i], cell: i });
    }
  }
  if (state.board.every(c => c === 'empty')) history = [];
}

function renderHistory() {
  if (history.length === 0) {
    histEl.innerHTML = '<li class="empty">No moves yet.</li>';
    return;
  }
  histEl.innerHTML = history.map((h, i) => `
    <li>
      <span class="n">${String(i + 1).padStart(2, '0')}</span>
      <span class="m ${h.mark}">${h.mark.toUpperCase()}</span>
      <span class="at">cell ${h.cell} &middot; you'd type ${h.cell + 1}</span>
    </li>`).join('');
  histEl.scrollTop = histEl.scrollHeight;
}

// --- talking to your C++ ----------------------------------------------------
const ERROR_TEXT = {
  cell_taken:   'That square is already taken.',
  out_of_range: 'That is not a square on the board.',
  game_over:    'This game has finished. Start a new one.',
  bad_request:  'The browser sent something the server could not read.',
};

function note(text, isError) {
  msgEl.textContent = text;
  msgEl.className = isError ? 'msg error' : 'msg';
}

function setConnected(up, label) {
  connDot.className = 'dot ' + (up ? 'up' : 'down');
  connText.textContent = label;
}

async function send(url, body) {
  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body ?? {}),
    });
    const payload = await response.json();
    setConnected(true, 'connected');

    if (payload.error && payload.error !== 'none') {
      note(ERROR_TEXT[payload.error] || payload.error, true);
    } else {
      note('Click an empty cell to play.', false);
    }
    render(payload.state);
  } catch (err) {
    setConnected(false, 'offline');
    note('Lost contact with the server. Is ./ttt serve still running?', true);
  }
}

async function load() {
  try {
    const response = await fetch('/api/state');
    render(await response.json());
    setConnected(true, 'connected');
  } catch (err) {
    setConnected(false, 'offline');
    note('Could not reach the server. Start it with ./ttt serve', true);
  }
}

load();
