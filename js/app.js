/**
 * js/app.js
 * Application controller: routing, screen management, UI binding, and event handling.
 */

const App = {
  currentScreen: 'home',

  init() {
    // Initialize Theme
    window.Theme.init();

    // Check QUIZ_DATA
    if (!window.QUIZ_DATA) {
      console.error('Quiz data is missing! Make sure data/quiz-data.js is loaded.');
    }

    this.bindEvents();
    this.showHomeScreen();
  },

  bindEvents() {
    // Theme toggle button
    const themeBtn = document.getElementById('theme-toggle-btn');
    if (themeBtn) {
      themeBtn.addEventListener('click', () => {
        window.Theme.toggle();
      });
    }

    // Settings checkboxes
    const shuffleCheckbox = document.getElementById('setting-shuffle');
    if (shuffleCheckbox) {
      const state = window.Storage.loadState();
      shuffleCheckbox.checked = Boolean(state.settings.shuffleQuestions);
      shuffleCheckbox.addEventListener('change', (e) => {
        const s = window.Storage.loadState();
        s.settings.shuffleQuestions = e.target.checked;
        window.Storage.saveState(s);
      });
    }

    const challengeCheckbox = document.getElementById('setting-challenge');
    if (challengeCheckbox) {
      const state = window.Storage.loadState();
      challengeCheckbox.checked = Boolean(state.settings.challengeMode);
      challengeCheckbox.addEventListener('change', (e) => {
        const s = window.Storage.loadState();
        s.settings.challengeMode = e.target.checked;
        window.Storage.saveState(s);
      });
    }

    // Reset Progress button
    const resetBtn = document.getElementById('reset-progress-btn');
    const resetDialog = document.getElementById('reset-confirm-dialog');
    const resetCancel = document.getElementById('reset-cancel-btn');
    const resetConfirm = document.getElementById('reset-confirm-btn');

    if (resetBtn && resetDialog) {
      resetBtn.addEventListener('click', () => {
        resetDialog.classList.remove('hidden');
      });
    }
    if (resetCancel && resetDialog) {
      resetCancel.addEventListener('click', () => {
        resetDialog.classList.add('hidden');
      });
    }
    if (resetConfirm && resetDialog) {
      resetConfirm.addEventListener('click', () => {
        window.Storage.resetState();
        resetDialog.classList.add('hidden');
        this.showHomeScreen();
      });
    }

    // Mixed mode button
    const mixedBtn = document.getElementById('start-mixed-btn');
    if (mixedBtn) {
      mixedBtn.addEventListener('click', () => this.startMixedPractice());
    }

    // Review mode button
    const reviewBtn = document.getElementById('start-review-btn');
    if (reviewBtn) {
      reviewBtn.addEventListener('click', () => this.startReviewPractice());
    }

    // Quiz Header: Back to home
    const quizBackBtn = document.getElementById('quiz-back-btn');
    if (quizBackBtn) {
      quizBackBtn.addEventListener('click', () => {
        if (confirm('Leave current quiz session and return to home?')) {
          this.showHomeScreen();
        }
      });
    }

    // Results screen buttons
    const retryBtn = document.getElementById('results-retry-btn');
    if (retryBtn) {
      retryBtn.addEventListener('click', () => {
        const lastSession = window.Quiz.session;
        if (lastSession) {
          if (lastSession.weekId === 'mixed') {
            this.startMixedPractice();
          } else if (lastSession.weekId === 'review') {
            this.startReviewPractice();
          } else {
            this.startWeekPractice(lastSession.weekId);
          }
        } else {
          this.showHomeScreen();
        }
      });
    }

    const reviewMissedBtn = document.getElementById('results-review-missed-btn');
    if (reviewMissedBtn) {
      reviewMissedBtn.addEventListener('click', () => {
        this.startReviewPractice();
      });
    }

    const resultsHomeBtn = document.getElementById('results-home-btn');
    if (resultsHomeBtn) {
      resultsHomeBtn.addEventListener('click', () => {
        this.showHomeScreen();
      });
    }

    // Lightbox modal close triggers
    const lightboxModal = document.getElementById('lightbox-modal');
    const lightboxClose = document.getElementById('lightbox-close-btn');
    if (lightboxClose) {
      lightboxClose.addEventListener('click', () => window.Quiz.closeLightbox());
    }
    if (lightboxModal) {
      lightboxModal.addEventListener('click', (e) => {
        if (e.target === lightboxModal) {
          window.Quiz.closeLightbox();
        }
      });
    }

    // Global keyboard listener
    window.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        const lightboxModal = document.getElementById('lightbox-modal');
        if (lightboxModal && !lightboxModal.classList.contains('hidden')) {
          window.Quiz.closeLightbox();
          return;
        }
        const resetDialog = document.getElementById('reset-confirm-dialog');
        if (resetDialog && !resetDialog.classList.contains('hidden')) {
          resetDialog.classList.add('hidden');
          return;
        }
      }
      window.Quiz.handleKeydown(e);
    });
  },

  switchScreen(screenId) {
    this.currentScreen = screenId;
    ['home-screen', 'quiz-screen', 'results-screen'].forEach((id) => {
      const el = document.getElementById(id);
      if (el) {
        if (id === `${screenId}-screen`) {
          el.classList.remove('hidden');
        } else {
          el.classList.add('hidden');
        }
      }
    });
    window.scrollTo(0, 0);
  },

  showHomeScreen() {
    this.switchScreen('home');
    const state = window.Storage.loadState();
    window.Game.updateDailyStreak(state);

    // Update Stats Header
    const levelInfo = window.Game.getLevelInfo(state.totalXp);
    const levelVal = document.getElementById('home-level-val');
    const xpVal = document.getElementById('home-xp-val');
    const xpProgress = document.getElementById('home-xp-bar-fill');
    const dailyStreakVal = document.getElementById('home-daily-streak-val');
    const bestStreakVal = document.getElementById('home-best-streak-val');

    if (levelVal) levelVal.textContent = `Level ${levelInfo.level}`;
    if (xpVal) xpVal.textContent = `${state.totalXp} XP (${levelInfo.currentLevelXp}/${levelInfo.nextLevelXp})`;
    if (xpProgress) xpProgress.style.width = `${levelInfo.progressPercent}%`;
    if (dailyStreakVal) dailyStreakVal.textContent = `${state.dailyStreak || 0}d`;
    if (bestStreakVal) bestStreakVal.textContent = `${state.bestStreak || 0}`;

    // Render Review Mode card count
    const wrongCount = (state.wrongQuestionIds || []).length;
    const reviewBtn = document.getElementById('start-review-btn');
    const reviewCountBadge = document.getElementById('review-count-badge');
    if (reviewBtn) {
      reviewBtn.disabled = wrongCount === 0;
    }
    if (reviewCountBadge) {
      reviewCountBadge.textContent = `${wrongCount} missed`;
    }

    // Render Week Grid (1 to 11)
    const grid = document.getElementById('week-grid');
    if (grid) {
      grid.innerHTML = '';
      for (let w = 1; w <= 11; w++) {
        const wKey = String(w);
        const weekInfo = state.completedWeeks[wKey];
        const card = document.createElement('button');
        card.type = 'button';
        card.className = 'week-card';
        if (weekInfo) card.classList.add('completed');

        const title = document.createElement('span');
        title.className = 'week-card-title';
        title.textContent = `Week ${w}`;

        const sub = document.createElement('span');
        sub.className = 'week-card-sub';
        if (weekInfo) {
          sub.textContent = `${weekInfo.bestScore}/${weekInfo.total} (${weekInfo.accuracy}%)`;
        } else {
          sub.textContent = '10 Questions';
        }

        const starsContainer = document.createElement('span');
        starsContainer.className = 'week-card-stars';
        const stars = weekInfo ? weekInfo.stars : 0;
        let starStr = '';
        for (let s = 1; s <= 3; s++) {
          starStr += s <= stars ? '★' : '☆';
        }
        starsContainer.textContent = starStr;

        card.appendChild(title);
        card.appendChild(sub);
        card.appendChild(starsContainer);

        card.addEventListener('click', () => {
          this.startWeekPractice(w);
        });

        grid.appendChild(card);
      }
    }

    // Render Badges Shelf
    const badgesContainer = document.getElementById('badges-shelf');
    if (badgesContainer) {
      badgesContainer.innerHTML = '';
      window.Game.BADGES.forEach((badge) => {
        const isUnlocked = state.badges.includes(badge.id);
        const badgeEl = document.createElement('div');
        badgeEl.className = `badge-item ${isUnlocked ? 'unlocked' : 'locked'}`;
        badgeEl.title = `${badge.name}: ${badge.description}`;

        const iconEl = document.createElement('span');
        iconEl.className = 'badge-icon';
        iconEl.textContent = badge.icon;

        const nameEl = document.createElement('span');
        nameEl.className = 'badge-name';
        nameEl.textContent = badge.name;

        badgeEl.appendChild(iconEl);
        badgeEl.appendChild(nameEl);
        badgesContainer.appendChild(badgeEl);
      });
    }
  },

  startWeekPractice(weekNum) {
    const questions = window.QUIZ_DATA[String(weekNum)];
    if (!questions || questions.length === 0) {
      alert(`No questions found for Week ${weekNum}`);
      return;
    }

    const state = window.Storage.loadState();
    this.switchScreen('quiz');

    const titleEl = document.getElementById('quiz-title');
    if (titleEl) titleEl.textContent = `Week ${weekNum} Practice`;

    window.Quiz.start({
      weekId: String(weekNum),
      questions: questions,
      isChallenge: Boolean(state.settings.challengeMode),
      isShuffled: Boolean(state.settings.shuffleQuestions)
    });
  },

  startMixedPractice() {
    const state = window.Storage.loadState();
    let allQuestions = [];
    for (let w = 1; w <= 11; w++) {
      const list = window.QUIZ_DATA[String(w)] || [];
      allQuestions = allQuestions.concat(list);
    }

    if (allQuestions.length === 0) {
      alert('No questions available.');
      return;
    }

    this.switchScreen('quiz');
    const titleEl = document.getElementById('quiz-title');
    if (titleEl) titleEl.textContent = 'Mixed Practice (All Weeks)';

    window.Quiz.start({
      weekId: 'mixed',
      questions: allQuestions,
      isChallenge: Boolean(state.settings.challengeMode),
      isShuffled: Boolean(state.settings.shuffleQuestions)
    });
  },

  startReviewPractice() {
    const state = window.Storage.loadState();
    const wrongIds = new Set(state.wrongQuestionIds || []);
    if (wrongIds.size === 0) {
      alert('No missed questions to review! Great job.');
      return;
    }

    let reviewQuestions = [];
    for (let w = 1; w <= 11; w++) {
      const list = window.QUIZ_DATA[String(w)] || [];
      list.forEach((q) => {
        if (wrongIds.has(q.id)) {
          reviewQuestions.push(q);
        }
      });
    }

    if (reviewQuestions.length === 0) {
      alert('Could not find question data for missed items.');
      return;
    }

    this.switchScreen('quiz');
    const titleEl = document.getElementById('quiz-title');
    if (titleEl) titleEl.textContent = `Review Mode (${reviewQuestions.length} Questions)`;

    window.Quiz.start({
      weekId: 'review',
      questions: reviewQuestions,
      isChallenge: Boolean(state.settings.challengeMode),
      isShuffled: false
    });
  },

  showResultsScreen(results) {
    this.switchScreen('results');

    const titleEl = document.getElementById('results-title');
    const scoreVal = document.getElementById('results-score-val');
    const accuracyVal = document.getElementById('results-accuracy-val');
    const xpVal = document.getElementById('results-xp-val');
    const streakVal = document.getElementById('results-streak-val');
    const starsContainer = document.getElementById('results-stars');
    const badgesSection = document.getElementById('results-new-badges');
    const reviewMissedBtn = document.getElementById('results-review-missed-btn');

    if (titleEl) {
      titleEl.textContent = results.isGameOver ? 'Challenge Over!' : 'Practice Complete!';
    }
    if (scoreVal) {
      scoreVal.textContent = `${results.firstAttemptScore} / ${results.totalQuestions}`;
    }
    if (accuracyVal) {
      accuracyVal.textContent = `${results.accuracy}%`;
    }
    if (xpVal) {
      xpVal.textContent = `+${results.earnedXp} XP`;
    }
    if (streakVal) {
      streakVal.textContent = `${results.bestStreak}`;
    }

    if (starsContainer) {
      let starStr = '';
      for (let s = 1; s <= 3; s++) {
        starStr += s <= results.stars ? '★' : '☆';
      }
      starsContainer.textContent = starStr;
    }

    // Show unlocked badges
    if (badgesSection) {
      badgesSection.innerHTML = '';
      if (results.newlyUnlockedBadges && results.newlyUnlockedBadges.length > 0) {
        const heading = document.createElement('h3');
        heading.className = 'results-badges-heading';
        heading.textContent = 'New Badges Unlocked!';
        badgesSection.appendChild(heading);

        const list = document.createElement('div');
        list.className = 'results-badges-list';
        results.newlyUnlockedBadges.forEach((bId) => {
          const badgeCfg = window.Game.BADGES.find((b) => b.id === bId);
          if (badgeCfg) {
            const badgeItem = document.createElement('div');
            badgeItem.className = 'badge-item unlocked';
            badgeItem.innerHTML = `<span class="badge-icon">${badgeCfg.icon}</span><span class="badge-name">${badgeCfg.name}</span>`;
            list.appendChild(badgeItem);
          }
        });
        badgesSection.appendChild(list);
      }
    }

    // Toggle Review Missed button
    if (reviewMissedBtn) {
      const state = window.Storage.loadState();
      const hasMissed = (state.wrongQuestionIds || []).length > 0;
      reviewMissedBtn.style.display = hasMissed ? 'inline-block' : 'none';
    }
  }
};

window.App = App;

// Bootstrap on DOM ready
document.addEventListener('DOMContentLoaded', () => {
  window.App.init();
});
