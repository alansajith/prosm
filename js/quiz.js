/**
 * js/quiz.js
 * Quiz engine: question rendering, single/multi answer checks, keyboard controls,
 * lightbox, lives handling, and state progression.
 */

const Quiz = {
  session: null,

  start(options) {
    // options: { weekId: '1'|...|'mixed'|'review', questions: [...], isChallenge: bool, isShuffled: bool }
    let questions = [...options.questions];

    if (options.isShuffled) {
      questions = this.shuffleArray(questions);
    }

    this.session = {
      weekId: options.weekId,
      questions: questions,
      currentIndex: 0,
      totalQuestions: questions.length,
      firstAttemptCorrectCount: 0,
      currentStreak: 0,
      maxStreak: 0,
      earnedXp: 0,
      isChallenge: Boolean(options.isChallenge),
      lives: options.isChallenge ? 3 : null,
      questionState: null // state for current question
    };

    this.renderCurrentQuestion();
  },

  shuffleArray(arr) {
    const copy = [...arr];
    for (let i = copy.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [copy[i], copy[j]] = [copy[j], copy[i]];
    }
    return copy;
  },

  getCurrentQuestion() {
    if (!this.session) return null;
    return this.session.questions[this.session.currentIndex];
  },

  renderQuestionText(container, text) {
    container.innerHTML = '';
    if (!text) return;

    // Match URLs starting with http://, https://, or www.
    const urlRegex = /(https?:\/\/[^\s<>'\"()]+|www\.[^\s<>'\"()]+)/g;
    let lastIndex = 0;
    let match;

    while ((match = urlRegex.exec(text)) !== null) {
      if (match.index > lastIndex) {
        container.appendChild(document.createTextNode(text.slice(lastIndex, match.index)));
      }

      let url = match[0];
      let trailing = '';
      while (url.length > 0 && /[.,;:!?)\]}>\"']$/.test(url)) {
        trailing = url.slice(-1) + trailing;
        url = url.slice(0, -1);
      }

      if (url) {
        const a = document.createElement('a');
        a.href = url.startsWith('http') ? url : 'https://' + url;
        a.textContent = url;
        a.target = '_blank';
        a.rel = 'noopener noreferrer';
        a.className = 'quiz-question-link';
        container.appendChild(a);
      }

      if (trailing) {
        container.appendChild(document.createTextNode(trailing));
      }

      lastIndex = match.index + match[0].length;
    }

    if (lastIndex < text.length) {
      container.appendChild(document.createTextNode(text.slice(lastIndex)));
    }
  },

  renderCurrentQuestion() {
    if (!this.session) return;

    if (this.session.currentIndex >= this.session.totalQuestions) {
      this.finishSession();
      return;
    }

    const q = this.getCurrentQuestion();
    const index = this.session.currentIndex;

    // Reset current question state
    this.session.questionState = {
      attemptNumber: 0,
      isSolved: false,
      selectedOptions: new Set(),
      disabledOptions: new Set()
    };

    // Update Quiz Header UI
    this.updateHeaderUi();

    const weekNum = q.id && q.id.startsWith('w') ? parseInt(q.id.slice(1, 3), 10) : (this.session.weekId || 1);

    // Render Question Text (with active clickable links)
    const qTextEl = document.getElementById('quiz-question-text');
    if (qTextEl) {
      this.renderQuestionText(qTextEl, q.question.text);
    }

    // Render Question Images
    const qImgsEl = document.getElementById('quiz-question-images');
    if (qImgsEl) {
      qImgsEl.innerHTML = '';
      if (q.question.images && q.question.images.length > 0) {
        q.question.images.forEach((src) => {
          const wrapper = document.createElement('div');
          wrapper.className = 'figure-wrapper';
          const img = document.createElement('img');
          img.src = src;
          img.alt = `Figure for question ${q.number}, week ${weekNum}`;
          img.loading = 'eager';
          img.tabIndex = 0;
          img.addEventListener('click', () => this.openLightbox(src, img.alt));
          img.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' || e.key === ' ') {
              e.preventDefault();
              this.openLightbox(src, img.alt);
            }
          });
          wrapper.appendChild(img);
          qImgsEl.appendChild(wrapper);
        });
      }
    }

    // Preload next question image
    if (this.session.currentIndex + 1 < this.session.totalQuestions) {
      const nextQ = this.session.questions[this.session.currentIndex + 1];
      if (nextQ.question.images) {
        nextQ.question.images.forEach((src) => {
          const preload = new Image();
          preload.src = src;
        });
      }
    }

    // Render Options List
    const optionsContainer = document.getElementById('quiz-options-container');
    if (optionsContainer) {
      optionsContainer.innerHTML = '';
      const isMulti = q.type === 'multi';

      q.options.forEach((opt, optIndex) => {
        const btn = document.createElement('button');
        btn.type = 'button';
        btn.className = 'option-btn';
        btn.dataset.id = opt.id;
        btn.setAttribute('aria-pressed', 'false');

        // Shortcut key label (A, B, C, D)
        const keyLabel = document.createElement('span');
        keyLabel.className = 'option-key';
        keyLabel.textContent = opt.id;

        // Content
        const contentSpan = document.createElement('span');
        contentSpan.className = 'option-content';
        if (opt.text) {
          contentSpan.textContent = opt.text;
        }

        if (opt.image) {
          const optImg = document.createElement('img');
          optImg.src = opt.image;
          optImg.alt = `Option ${opt.id} figure for question ${q.number}, week ${weekNum}`;
          optImg.className = 'option-image';
          optImg.addEventListener('click', (e) => {
            e.stopPropagation();
            this.openLightbox(opt.image, optImg.alt);
          });
          contentSpan.appendChild(optImg);
        }

        // Status indicator icon (check or cross)
        const statusSpan = document.createElement('span');
        statusSpan.className = 'option-status-icon';
        statusSpan.setAttribute('aria-hidden', 'true');

        btn.appendChild(keyLabel);
        btn.appendChild(contentSpan);
        btn.appendChild(statusSpan);

        btn.addEventListener('click', () => {
          if (isMulti) {
            this.toggleMultiOption(opt.id, btn);
          } else {
            this.handleSingleSelect(opt.id, btn);
          }
        });

        optionsContainer.appendChild(btn);
      });
    }

    // Render Action Controls (Check / Next button)
    const actionContainer = document.getElementById('quiz-actions');
    if (actionContainer) {
      actionContainer.innerHTML = '';
      if (q.type === 'multi') {
        const checkBtn = document.createElement('button');
        checkBtn.type = 'button';
        checkBtn.id = 'quiz-check-btn';
        checkBtn.className = 'btn btn-primary';
        checkBtn.textContent = 'Check Answer';
        checkBtn.disabled = true;
        checkBtn.addEventListener('click', () => this.handleMultiSubmit());
        actionContainer.appendChild(checkBtn);
      }

      const nextBtn = document.createElement('button');
      nextBtn.type = 'button';
      nextBtn.id = 'quiz-next-btn';
      nextBtn.className = 'btn btn-secondary';
      nextBtn.textContent = index === this.session.totalQuestions - 1 ? 'Finish Quiz' : 'Next Question';
      nextBtn.style.display = 'none'; // hidden until correct
      nextBtn.addEventListener('click', () => this.goToNextQuestion());
      actionContainer.appendChild(nextBtn);
    }

    // Announce to screen reader
    this.announce(`Question ${index + 1} of ${this.session.totalQuestions}: ${q.question.text}`);
  },

  updateHeaderUi() {
    if (!this.session) return;
    const q = this.getCurrentQuestion();
    const progressEl = document.getElementById('quiz-progress-text');
    const progressBar = document.getElementById('quiz-progress-fill');
    const scoreEl = document.getElementById('quiz-score-val');
    const streakEl = document.getElementById('quiz-streak-val');
    const livesContainer = document.getElementById('quiz-lives-container');
    const livesEl = document.getElementById('quiz-lives-val');
    const typeBadge = document.getElementById('quiz-type-badge');

    if (progressEl) {
      progressEl.textContent = `Question ${this.session.currentIndex + 1} of ${this.session.totalQuestions}`;
    }
    if (progressBar) {
      const pct = Math.round((this.session.currentIndex / this.session.totalQuestions) * 100);
      progressBar.style.width = `${pct}%`;
    }
    if (scoreEl) {
      scoreEl.textContent = `${this.session.firstAttemptCorrectCount}`;
    }
    if (streakEl) {
      streakEl.textContent = `${this.session.currentStreak}`;
    }
    if (typeBadge) {
      typeBadge.textContent = q.type === 'multi' ? 'Select All That Apply' : 'Single Choice';
    }

    if (livesContainer && livesEl) {
      if (this.session.isChallenge) {
        livesContainer.style.display = 'flex';
        livesEl.textContent = '♥ '.repeat(this.session.lives).trim();
      } else {
        livesContainer.style.display = 'none';
      }
    }
  },

  announce(msg) {
    const el = document.getElementById('aria-live-announcer');
    if (el) {
      el.textContent = '';
      setTimeout(() => {
        el.textContent = msg;
      }, 50);
    }
  },

  // Single choice selection
  handleSingleSelect(optionId, buttonEl) {
    const qState = this.session.questionState;
    if (qState.isSolved || qState.disabledOptions.has(optionId)) return;

    qState.attemptNumber += 1;
    const q = this.getCurrentQuestion();
    const isCorrect = q.answer.includes(optionId) && q.answer.length === 1;

    if (isCorrect) {
      this.handleCorrect([optionId]);
    } else {
      this.handleWrong([optionId]);
    }
  },

  // Multi choice toggle
  toggleMultiOption(optionId, buttonEl) {
    const qState = this.session.questionState;
    if (qState.isSolved || qState.disabledOptions.has(optionId)) return;

    if (qState.selectedOptions.has(optionId)) {
      qState.selectedOptions.delete(optionId);
      buttonEl.classList.remove('selected');
      buttonEl.setAttribute('aria-pressed', 'false');
    } else {
      qState.selectedOptions.add(optionId);
      buttonEl.classList.add('selected');
      buttonEl.setAttribute('aria-pressed', 'true');
    }

    const checkBtn = document.getElementById('quiz-check-btn');
    if (checkBtn) {
      checkBtn.disabled = qState.selectedOptions.size === 0;
    }
  },

  // Multi choice submit check
  handleMultiSubmit() {
    const qState = this.session.questionState;
    if (qState.isSolved || qState.selectedOptions.size === 0) return;

    qState.attemptNumber += 1;
    const q = this.getCurrentQuestion();
    const selected = Array.from(qState.selectedOptions);
    const correctSet = new Set(q.answer);

    const isMatch =
      selected.length === correctSet.size &&
      selected.every((id) => correctSet.has(id));

    if (isMatch) {
      this.handleCorrect(selected);
    } else {
      this.handleMultiWrong(selected);
    }
  },

  handleMultiWrong(selected) {
    const qState = this.session.questionState;
    qState.isSolved = true;
    const isFirstAttempt = qState.attemptNumber === 1;
    const q = this.getCurrentQuestion();
    const correctAnswers = q.answer || [];
    const correctSet = new Set(correctAnswers);

    if (isFirstAttempt) {
      this.session.currentStreak = 0;

      // Record wrong question id in storage for review mode
      const state = window.Storage.loadState();
      if (!state.wrongQuestionIds.includes(q.id)) {
        state.wrongQuestionIds.push(q.id);
        window.Storage.saveState(state);
      }

      // If challenge mode, deduct life
      if (this.session.isChallenge) {
        this.session.lives -= 1;
        if (this.session.lives <= 0) {
          this.announce('Wrong. No lives remaining!');
          this.updateHeaderUi();
          setTimeout(() => {
            this.finishSession(true); // Game Over
          }, 800);
          return;
        }
      }
    }

    this.announce('Wrong');

    // Immediately give/reveal the correct options in accent color with checkmark
    correctAnswers.forEach((id) => {
      const btn = document.querySelector(`.option-btn[data-id="${id}"]`);
      if (btn) {
        btn.classList.add('correct');
        const icon = btn.querySelector('.option-status-icon');
        if (icon) icon.textContent = '✓';
      }
    });

    // Mark any incorrectly selected options as wrong with strike and shake
    selected.forEach((id) => {
      if (!correctSet.has(id)) {
        const btn = document.querySelector(`.option-btn[data-id="${id}"]`);
        if (btn) {
          btn.classList.add('wrong');
          btn.classList.add('shake');
          const icon = btn.querySelector('.option-status-icon');
          if (icon) icon.textContent = '✕';
          setTimeout(() => {
            btn.classList.remove('shake');
          }, 400);
        }
      }
    });

    // Disable all options
    document.querySelectorAll('.option-btn').forEach((b) => {
      b.disabled = true;
    });

    // Hide Check button and show Next Question button
    const checkBtn = document.getElementById('quiz-check-btn');
    if (checkBtn) checkBtn.style.display = 'none';

    const nextBtn = document.getElementById('quiz-next-btn');
    if (nextBtn) {
      nextBtn.style.display = 'inline-block';
      nextBtn.focus();
    }

    this.updateHeaderUi();
  },

  handleCorrect(optionIds) {
    const qState = this.session.questionState;
    qState.isSolved = true;
    const isFirstAttempt = qState.attemptNumber === 1;

    // Visual mark for correct options: accent background + check icon
    optionIds.forEach((id) => {
      const btn = document.querySelector(`.option-btn[data-id="${id}"]`);
      if (btn) {
        btn.classList.add('correct');
        const icon = btn.querySelector('.option-status-icon');
        if (icon) icon.textContent = '✓';
      }
    });

    // Disable all options
    document.querySelectorAll('.option-btn').forEach((b) => {
      b.disabled = true;
    });

    // Handle Scoring & XP (Only first attempt counts)
    if (isFirstAttempt) {
      this.session.firstAttemptCorrectCount += 1;
      this.session.currentStreak += 1;
      if (this.session.currentStreak > this.session.maxStreak) {
        this.session.maxStreak = this.session.currentStreak;
      }

      const xp = window.Game.calculateQuestionXp(this.session.currentStreak);
      this.session.earnedXp += xp;

      // Update storage XP and first_step badge
      const state = window.Storage.loadState();
      state.totalXp = (state.totalXp || 0) + xp;
      window.Game.unlockBadge(state, 'first_step');

      // If in review mode, remove question from wrong list
      const q = this.getCurrentQuestion();
      if (state.wrongQuestionIds.includes(q.id)) {
        state.wrongQuestionIds = state.wrongQuestionIds.filter((id) => id !== q.id);
      }
      window.Storage.saveState(state);
    } else {
      // Streak breaks if solved on subsequent attempt
      this.session.currentStreak = 0;
    }

    this.announce('Correct');
    this.updateHeaderUi();

    // Hide Check button, show Next button
    const checkBtn = document.getElementById('quiz-check-btn');
    if (checkBtn) checkBtn.style.display = 'none';

    const nextBtn = document.getElementById('quiz-next-btn');
    if (nextBtn) {
      nextBtn.style.display = 'inline-block';
      nextBtn.focus();
    }
  },

  handleWrong(optionIds) {
    const qState = this.session.questionState;
    const isFirstAttempt = qState.attemptNumber === 1;

    // On wrong first attempt
    if (isFirstAttempt) {
      this.session.currentStreak = 0;
      const q = this.getCurrentQuestion();

      // Record wrong question id in storage for review mode
      const state = window.Storage.loadState();
      if (!state.wrongQuestionIds.includes(q.id)) {
        state.wrongQuestionIds.push(q.id);
        window.Storage.saveState(state);
      }

      // If challenge mode, deduct life
      if (this.session.isChallenge) {
        this.session.lives -= 1;
        if (this.session.lives <= 0) {
          this.announce('Wrong. No lives remaining!');
          this.updateHeaderUi();
          setTimeout(() => {
            this.finishSession(true); // Game Over
          }, 800);
          return;
        }
      }
    }

    this.announce('Wrong');

    // Visual mark for wrong options: dashed border, ✕ icon, shake
    optionIds.forEach((id) => {
      const btn = document.querySelector(`.option-btn[data-id="${id}"]`);
      if (btn) {
        btn.classList.add('wrong');
        btn.classList.add('shake');
        const icon = btn.querySelector('.option-status-icon');
        if (icon) icon.textContent = '✕';

        // Once marked wrong, lock this option out
        qState.disabledOptions.add(id);
        qState.selectedOptions.delete(id);
        btn.classList.remove('selected');
        btn.disabled = true;

        setTimeout(() => {
          btn.classList.remove('shake');
        }, 500);
      }
    });

    const checkBtn = document.getElementById('quiz-check-btn');
    if (checkBtn) {
      checkBtn.disabled = qState.selectedOptions.size === 0;
    }

    this.updateHeaderUi();
  },

  goToNextQuestion() {
    this.session.currentIndex += 1;
    this.renderCurrentQuestion();
  },

  finishSession(isGameOver = false) {
    const session = this.session;
    const record = window.Game.recordWeekCompletion(
      session.weekId,
      session.firstAttemptCorrectCount,
      session.totalQuestions,
      session.maxStreak
    );

    window.App.showResultsScreen({
      weekId: session.weekId,
      firstAttemptScore: session.firstAttemptCorrectCount,
      totalQuestions: session.totalQuestions,
      accuracy: record.accuracy,
      stars: record.stars,
      earnedXp: session.earnedXp,
      bestStreak: session.maxStreak,
      isGameOver: isGameOver,
      newlyUnlockedBadges: record.newlyUnlockedBadges,
      hasWrongQuestions: session.firstAttemptCorrectCount < session.totalQuestions
    });
  },

  // Keyboard shortcut listener
  handleKeydown(e) {
    if (!this.session || document.getElementById('quiz-screen')?.classList.contains('hidden')) {
      return;
    }

    // Do not hijack keyboard events if user is focused on an interactive link
    if (document.activeElement && document.activeElement.tagName === 'A') {
      return;
    }

    // Lightbox Escape
    const lightbox = document.getElementById('lightbox-modal');
    if (lightbox && !lightbox.classList.contains('hidden')) {
      if (e.key === 'Escape') {
        this.closeLightbox();
      }
      return;
    }

    const nextBtn = document.getElementById('quiz-next-btn');
    if (nextBtn && nextBtn.style.display !== 'none') {
      if (e.key === 'Enter') {
        e.preventDefault();
        nextBtn.click();
        return;
      }
    }

    const checkBtn = document.getElementById('quiz-check-btn');
    if (checkBtn && checkBtn.style.display !== 'none' && !checkBtn.disabled) {
      if (e.key === 'Enter') {
        e.preventDefault();
        checkBtn.click();
        return;
      }
    }

    // Map keys A-D or 1-4
    const key = e.key.toUpperCase();
    const map = { '1': 'A', '2': 'B', '3': 'C', '4': 'D', 'A': 'A', 'B': 'B', 'C': 'C', 'D': 'D' };
    const optId = map[key];

    if (optId) {
      const btn = document.querySelector(`.option-btn[data-id="${optId}"]`);
      if (btn && !btn.disabled) {
        e.preventDefault();
        btn.click();
      }
    }
  },

  openLightbox(src, alt) {
    const modal = document.getElementById('lightbox-modal');
    const img = document.getElementById('lightbox-img');
    const caption = document.getElementById('lightbox-caption');
    if (!modal || !img) return;

    img.src = src;
    img.alt = alt || 'Enlarged figure';
    if (caption) caption.textContent = alt || '';

    modal.classList.remove('hidden');
    document.body.style.overflow = 'hidden';
    modal.focus();
  },

  closeLightbox() {
    const modal = document.getElementById('lightbox-modal');
    if (!modal) return;
    modal.classList.add('hidden');
    document.body.style.overflow = '';
  }
};

window.Quiz = Quiz;
