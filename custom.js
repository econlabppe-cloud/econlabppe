/* ============================================================
   EconLabPPE — Gamification JavaScript
   Progress Tracking + Confetti + UI Enhancements
   ============================================================ */

(function () {
  'use strict';

  /* ── Constants ── */
  const TOTAL_WEEKS    = 22;
  const STORAGE_KEY    = 'econlab_progress_v2';
  const CONFETTI_CDN   = 'https://cdn.jsdelivr.net/npm/canvas-confetti@1.9.3/dist/confetti.browser.min.js';

  /* Map URL path segments → canonical week IDs */
  const WEEK_MAP = {
    'Week_01_Setup':                    'week_01',
    'Week_02_Excel_Basics':             'week_02',
    'Week_03_Excel_Intermediate':       'week_03',
    'Week_04_Excel_Advanced':           'week_04',
    'Week_05_SQL_Basics':               'week_05',
    'Week_06_SQL_Intermediate':         'week_06',
    'Week_07_SQL_Advanced':             'week_07',
    'Week_08_Python_Basics':            'week_08',
    'Week_09_Pandas_Basics':            'week_09',
    'Week_10_Pandas_Advanced':          'week_10',
    'Week_11_APIs_Israel':              'week_11',
    'Week_12_APIs_International':       'week_12',
    'Week_13_R_Basics':                 'week_13',
    'Week_14_R_Tidyverse':              'week_14',
    'Week_15_Econometrics_Regression':  'week_15',
    'Week_16_Econometrics_Advanced':    'week_16',
    'Week_17_Visualization_Python':     'week_17',
    'Week_18_Visualization_R':          'week_18',
    'Week_19_BI_PowerBI':               'week_19',
    'Week_20_BI_Tableau':               'week_20',
    'Week_21_DSGE_Intro':               'week_21',
    'Week_22_DSGE_Advanced':            'week_22',
  };

  /* ── Storage helpers ── */
  function getProgress() {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      return raw ? JSON.parse(raw) : {};
    } catch (_) { return {}; }
  }

  function markWeekDone(weekId) {
    try {
      const p = getProgress();
      if (!p[weekId]) {
        p[weekId] = { done: true, ts: Date.now() };
        localStorage.setItem(STORAGE_KEY, JSON.stringify(p));
      }
    } catch (_) {}
  }

  function getCompletedCount() {
    return Object.keys(getProgress()).length;
  }

  function isWeekDone(weekId) {
    return !!getProgress()[weekId];
  }

  /* ── Detect current week from URL ── */
  function detectWeekId() {
    const path = window.location.pathname;
    for (const [folder, id] of Object.entries(WEEK_MAP)) {
      if (path.includes(folder)) return id;
    }
    // Fallback: match Week_NN pattern
    const m = path.match(/Week_(\d{2})/);
    return m ? `week_${m[1]}` : null;
  }

  /* ── Load canvas-confetti lazily ── */
  function loadConfetti() {
    return new Promise((resolve) => {
      if (window.confetti) { resolve(window.confetti); return; }
      const s = document.createElement('script');
      s.src = CONFETTI_CDN;
      s.onload = () => resolve(window.confetti);
      s.onerror = () => resolve(null);         // graceful degradation
      document.head.appendChild(s);
    });
  }

  /* ── Fire confetti burst ── */
  async function fireCelebration() {
    const confetti = await loadConfetti();
    if (!confetti) return;

    const defaults = { zIndex: 9999, disableForReducedMotion: true };

    function burst(ratio, opts) {
      confetti(Object.assign({}, defaults, opts, {
        particleCount: Math.floor(200 * ratio),
      }));
    }

    burst(0.25, { spread: 26, startVelocity: 55, origin: { y: 0.6 } });
    burst(0.20, { spread: 60,  origin: { y: 0.65 } });
    burst(0.35, { spread: 100, decay: 0.91, scalar: 0.8, origin: { y: 0.7 } });
    burst(0.10, { spread: 120, startVelocity: 25, decay: 0.92, scalar: 1.2, origin: { y: 0.75 } });
    burst(0.10, { spread: 120, startVelocity: 45, origin: { y: 0.6 } });

    // Bonus side bursts
    setTimeout(() => {
      confetti(Object.assign({}, defaults, {
        particleCount: 60, angle: 60, spread: 55, origin: { x: 0, y: 0.65 }
      }));
      confetti(Object.assign({}, defaults, {
        particleCount: 60, angle: 120, spread: 55, origin: { x: 1, y: 0.65 }
      }));
    }, 250);
  }

  /* ── Build progress bar HTML ── */
  function buildProgressBar(compact = false) {
    const done = getCompletedCount();
    const pct  = Math.round((done / TOTAL_WEEKS) * 100);
    const stars = done >= 22 ? ' 🌟' : done >= 15 ? ' ⭐' : done >= 7 ? ' 🔥' : '';

    return `
      <div id="econlab-progress-container">
        <div id="econlab-progress-header">
          <span id="econlab-progress-label">📊 ההתקדמות שלך${stars}</span>
          <span id="econlab-progress-text">${done}/${TOTAL_WEEKS} שבועות</span>
        </div>
        <div id="econlab-progress-bar-bg">
          <div id="econlab-progress-bar" style="width:${pct}%"></div>
        </div>
        <div id="econlab-progress-footer">
          <span>${pct === 0 ? 'בואו נתחיל! 💪' : pct === 100 ? '🎉 השלמת את הקורס!' : `${pct}% הושלם`}</span>
          <span style="opacity:0.75;font-size:0.7rem">מתאפס עם ניקוי Cache</span>
        </div>
      </div>`;
  }

  /* ── Inject progress bar into sidebar ── */
  function injectProgressBar() {
    // Don't double-inject
    if (document.getElementById('econlab-progress-container')) return;

    const html = buildProgressBar();
    const wrap = document.createElement('div');
    wrap.innerHTML = html;

    // Try sidebar first, then fallback positions
    const targets = [
      '#quarto-sidebar .sidebar-menu-container',
      '#quarto-sidebar',
      '.sidebar-nav',
      '.sidebar',
    ];

    for (const sel of targets) {
      const el = document.querySelector(sel);
      if (el) {
        el.insertBefore(wrap.firstElementChild, el.firstChild);
        return;
      }
    }

    // Last resort: top of page
    const main = document.querySelector('#quarto-content') || document.querySelector('main');
    if (main) main.insertBefore(wrap.firstElementChild, main.firstChild);
  }

  /* ── Inject standalone progress bar for index page ── */
  function injectGlobalProgressBar() {
    const wrapper = document.getElementById('econlab-global-progress-wrapper');
    if (!wrapper) return;
    wrapper.innerHTML = buildProgressBar();
  }

  /* ── Refresh all progress UI elements ── */
  function refreshProgressUI() {
    const done = getCompletedCount();
    const pct  = Math.round((done / TOTAL_WEEKS) * 100);

    const bar   = document.getElementById('econlab-progress-bar');
    const text  = document.getElementById('econlab-progress-text');
    const foot  = document.querySelector('#econlab-progress-footer span:first-child');
    const label = document.getElementById('econlab-progress-label');

    if (bar)   bar.style.width = pct + '%';
    if (text)  text.textContent = `${done}/${TOTAL_WEEKS} שבועות`;
    if (foot)  foot.textContent = pct === 100 ? '🎉 השלמת את הקורס!' : `${pct}% הושלם`;
    if (label) {
      const stars = done >= 22 ? ' 🌟' : done >= 15 ? ' ⭐' : done >= 7 ? ' 🔥' : '';
      label.textContent = `📊 ההתקדמות שלך${stars}`;
    }
  }

  /* ── Build "I finished this week!" button HTML ── */
  function buildFinishButton(weekId) {
    const done = isWeekDone(weekId);
    return `
      <div id="econlab-finish-container">
        <hr style="margin-bottom:1.5rem;opacity:0.15;">
        ${done ? `
          <button id="econlab-finish-btn" class="completed" disabled>
            ✅ שבוע זה הושלם!
          </button>
          <p class="econlab-completed-msg">כל הכבוד! המשיכו לשבוע הבא 🚀</p>
        ` : `
          <button id="econlab-finish-btn" onclick="window.__econlab.finishWeek()">
            ✅ סיימתי את השבוע!
          </button>
          <p class="econlab-finish-desc">לחצו לאחר השלמת כל המשימות — תקבלו ציון ו-XP!</p>
        `}
      </div>`;
  }

  /* ── Inject finish button at bottom of assignment pages ── */
  function injectFinishButton() {
    if (document.getElementById('econlab-finish-container')) return;

    const weekId = detectWeekId();
    if (!weekId) return;

    const html = buildFinishButton(weekId);
    const wrap = document.createElement('div');
    wrap.innerHTML = html;

    const targets = [
      '.page-navigation',
      '#quarto-content',
      'main .container-fluid',
      'main',
    ];

    for (const sel of targets) {
      const el = document.querySelector(sel);
      if (el) {
        el.parentNode.insertBefore(wrap.firstElementChild, el);
        return;
      }
    }
  }

  /* ── Handle finish click (exposed globally for onclick attr) ── */
  async function handleFinishWeek() {
    const weekId = detectWeekId();
    if (!weekId || isWeekDone(weekId)) return;

    markWeekDone(weekId);

    // Update button immediately
    const btn       = document.getElementById('econlab-finish-btn');
    const container = document.getElementById('econlab-finish-container');

    if (btn) {
      btn.disabled    = true;
      btn.textContent = '✅ שבוע זה הושלם!';
      btn.classList.add('completed');
    }

    if (container) {
      const desc = container.querySelector('.econlab-finish-desc');
      if (desc) desc.remove();

      if (!container.querySelector('.econlab-completed-msg')) {
        const msg = document.createElement('p');
        msg.className   = 'econlab-completed-msg';
        msg.textContent = 'כל הכבוד! המשיכו לשבוע הבא 🚀';
        container.appendChild(msg);
      }
    }

    refreshProgressUI();
    await fireCelebration();
  }

  /* ── Enhance Code Copy button label (Hebrew) ── */
  function enhanceCodeCopyButtons() {
    // Quarto renders copy buttons; we add a tooltip/title override
    document.querySelectorAll('.code-copy-button').forEach((btn) => {
      if (!btn.dataset.econlabPatched) {
        btn.title = 'העתק קוד';
        btn.dataset.econlabPatched = 'true';

        btn.addEventListener('click', () => {
          const original = btn.innerHTML;
          btn.innerHTML = '✓ הועתק!';
          setTimeout(() => { btn.innerHTML = original; }, 2000);
        });
      }
    });
  }

  /* ── Animate sidebar active item on load ── */
  function highlightActiveSidebarItem() {
    const active = document.querySelector('.sidebar-item.active a, .active.nav-link');
    if (active) {
      active.style.fontWeight = '700';
      active.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
    }
  }

  /* ── Smooth progress bar entrance animation ── */
  function animateProgressBarEntrance() {
    const bar = document.getElementById('econlab-progress-bar');
    if (!bar) return;
    const targetWidth = bar.style.width;
    bar.style.width = '0%';
    requestAnimationFrame(() => {
      requestAnimationFrame(() => {
        bar.style.width = targetWidth;
      });
    });
  }

  /* ── Detect assignment page ── */
  function isAssignmentPage() {
    const path = window.location.pathname;
    return Object.keys(WEEK_MAP).some((folder) => path.includes(folder)) ||
           /Week_\d{2}/.test(path);
  }

  /* ── Main init ── */
  function init() {
    injectProgressBar();
    injectGlobalProgressBar();
    animateProgressBarEntrance();

    if (isAssignmentPage()) {
      injectFinishButton();
    }

    enhanceCodeCopyButtons();
    highlightActiveSidebarItem();

    // Re-patch copy buttons if code blocks load lazily
    const obs = new MutationObserver(() => enhanceCodeCopyButtons());
    obs.observe(document.body, { childList: true, subtree: true });
  }

  /* ── Expose public API ── */
  window.__econlab = {
    finishWeek:   handleFinishWeek,
    getProgress:  getProgress,
    getCompleted: getCompletedCount,
    resetProgress: function () {
      localStorage.removeItem(STORAGE_KEY);
      refreshProgressUI();
      console.info('[EconLabPPE] Progress reset.');
    },
  };

  /* ── Bootstrap ── */
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

})();
