/**
 * js/game.js
 * Gamification engine: XP, streaks, levels, stars, badges, and progress.
 */

const BADGES_CONFIG = [
  {
    id: 'first_step',
    name: 'First Step',
    description: 'Answer your first question correctly',
    icon: '✦'
  },
  {
    id: 'streak_5',
    name: 'On Fire',
    description: 'Achieve a 5-question answer streak',
    icon: '⚡'
  },
  {
    id: 'streak_10',
    name: 'Unstoppable',
    description: 'Achieve a 10-question answer streak',
    icon: '★'
  },
  {
    id: 'streak_20',
    name: 'Mastermind',
    description: 'Achieve a 20-question answer streak',
    icon: '♦'
  },
  {
    id: 'week_done',
    name: 'Week Finisher',
    description: 'Complete any week practice set',
    icon: '✓'
  },
  {
    id: 'week_master',
    name: 'Week Master',
    description: 'Earn 3 stars (≥95% accuracy) on a week',
    icon: '✪'
  },
  {
    id: 'all_weeks',
    name: 'Grandmaster',
    description: 'Complete all 11 weeks of practice',
    icon: '▲'
  },
  {
    id: 'daily_7',
    name: 'Dedication',
    description: 'Practise 7 days in a row',
    icon: '☯'
  }
];

const Game = {
  BADGES: BADGES_CONFIG,

  // Calculate level and XP progress
  // Level N requires N * 100 XP
  getLevelInfo(totalXp) {
    const xp = Math.max(0, totalXp || 0);
    // Simple level formula: 100 XP per level
    const level = Math.floor(xp / 100) + 1;
    const currentLevelXp = xp % 100;
    const nextLevelXp = 100;
    const progressPercent = Math.min(100, Math.floor((currentLevelXp / nextLevelXp) * 100));
    return { level, currentLevelXp, nextLevelXp, progressPercent };
  },

  // Calculate multiplier based on streak
  getMultiplier(streak) {
    if (streak >= 15) return 2.5;
    if (streak >= 10) return 2.0;
    if (streak >= 5) return 1.5;
    return 1.0;
  },

  // Calculate XP gained for a correct answer on first attempt
  calculateQuestionXp(streak) {
    const base = 10;
    const mult = this.getMultiplier(streak);
    return Math.round(base * mult);
  },

  // Calculate star rating (0-3) for accuracy
  calculateStars(accuracy) {
    if (accuracy >= 95) return 3;
    if (accuracy >= 80) return 2;
    if (accuracy >= 60) return 1;
    return 0;
  },

  // Check and update daily streak on user activity
  updateDailyStreak(state) {
    const today = new Date().toISOString().split('T')[0];
    const lastPlayed = state.lastPlayedDate;

    if (!lastPlayed) {
      state.dailyStreak = 1;
      state.lastPlayedDate = today;
    } else if (lastPlayed !== today) {
      const yesterday = new Date(Date.now() - 86400000).toISOString().split('T')[0];
      if (lastPlayed === yesterday) {
        state.dailyStreak = (state.dailyStreak || 0) + 1;
      } else {
        // Streak broken
        state.dailyStreak = 1;
      }
      state.lastPlayedDate = today;
    }

    if (state.dailyStreak >= 7) {
      this.unlockBadge(state, 'daily_7');
    }
  },

  // Unlock a badge if not already unlocked. Returns true if newly unlocked.
  unlockBadge(state, badgeId) {
    if (!state.badges.includes(badgeId)) {
      state.badges.push(badgeId);
      return true;
    }
    return false;
  },

  // Process end of session / week completion
  recordWeekCompletion(weekNum, correctFirstAttempts, totalQuestions, sessionMaxStreak) {
    const state = window.Storage.loadState();
    const accuracy = totalQuestions > 0 ? Math.round((correctFirstAttempts / totalQuestions) * 100) : 0;
    const stars = this.calculateStars(accuracy);
    const newlyUnlockedBadges = [];

    this.updateDailyStreak(state);

    // Update best streak
    if (sessionMaxStreak > (state.bestStreak || 0)) {
      state.bestStreak = sessionMaxStreak;
    }

    // Check streak badges
    if (sessionMaxStreak >= 5 && this.unlockBadge(state, 'streak_5')) newlyUnlockedBadges.push('streak_5');
    if (sessionMaxStreak >= 10 && this.unlockBadge(state, 'streak_10')) newlyUnlockedBadges.push('streak_10');
    if (sessionMaxStreak >= 20 && this.unlockBadge(state, 'streak_20')) newlyUnlockedBadges.push('streak_20');

    if (weekNum !== 'mixed' && weekNum !== 'review') {
      const wKey = String(weekNum);
      const prev = state.completedWeeks[wKey] || { bestScore: 0, accuracy: 0, stars: 0 };

      state.completedWeeks[wKey] = {
        bestScore: Math.max(prev.bestScore || 0, correctFirstAttempts),
        total: totalQuestions,
        accuracy: Math.max(prev.accuracy || 0, accuracy),
        stars: Math.max(prev.stars || 0, stars),
        completedAt: new Date().toISOString()
      };

      if (this.unlockBadge(state, 'week_done')) newlyUnlockedBadges.push('week_done');
      if (stars === 3 && this.unlockBadge(state, 'week_master')) newlyUnlockedBadges.push('week_master');

      // Check if all 11 weeks completed
      let allDone = true;
      for (let i = 1; i <= 11; i++) {
        if (!state.completedWeeks[String(i)]) {
          allDone = false;
          break;
        }
      }
      if (allDone && this.unlockBadge(state, 'all_weeks')) newlyUnlockedBadges.push('all_weeks');
    }

    window.Storage.saveState(state);
    return {
      accuracy,
      stars,
      newlyUnlockedBadges,
      totalXp: state.totalXp,
      dailyStreak: state.dailyStreak
    };
  }
};

window.Game = Game;
