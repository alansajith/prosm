/**
 * js/storage.js
 * Safe localStorage wrapper with try/catch fallback and state schema.
 */

const STORAGE_KEY = 'mcqPractice.v1';

const DEFAULT_STATE = {
  totalXp: 0,
  streak: 0,
  bestStreak: 0,
  dailyStreak: 0,
  lastPlayedDate: null,
  completedWeeks: {}, // { "1": { bestScore: 9, total: 10, accuracy: 90, stars: 2, completedAt: "..." } }
  badges: [], // list of unlocked badge IDs
  wrongQuestionIds: [], // unique list of question IDs answered wrong on first attempt
  settings: {
    theme: 'auto', // 'auto' | 'light' | 'dark'
    shuffleQuestions: false,
    challengeMode: false // 3 lives mode
  }
};

const Storage = {
  isAvailable() {
    try {
      const test = '__storage_test__';
      localStorage.setItem(test, test);
      localStorage.removeItem(test);
      return true;
    } catch (e) {
      return false;
    }
  },

  loadState() {
    try {
      if (!this.isAvailable()) {
        return JSON.parse(JSON.stringify(DEFAULT_STATE));
      }
      const raw = localStorage.getItem(STORAGE_KEY);
      if (!raw) {
        return JSON.parse(JSON.stringify(DEFAULT_STATE));
      }
      const parsed = JSON.parse(raw);
      // Merge with default state to ensure all keys exist
      return {
        ...DEFAULT_STATE,
        ...parsed,
        completedWeeks: { ...DEFAULT_STATE.completedWeeks, ...(parsed.completedWeeks || {}) },
        settings: { ...DEFAULT_STATE.settings, ...(parsed.settings || {}) },
        badges: Array.isArray(parsed.badges) ? parsed.badges : [],
        wrongQuestionIds: Array.isArray(parsed.wrongQuestionIds) ? parsed.wrongQuestionIds : []
      };
    } catch (e) {
      console.warn('Error reading from localStorage, using default state:', e);
      return JSON.parse(JSON.stringify(DEFAULT_STATE));
    }
  },

  saveState(state) {
    try {
      if (!this.isAvailable()) return false;
      localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
      return true;
    } catch (e) {
      console.warn('Error writing to localStorage:', e);
      return false;
    }
  },

  resetState() {
    try {
      if (this.isAvailable()) {
        localStorage.removeItem(STORAGE_KEY);
      }
    } catch (e) {
      console.warn('Error resetting localStorage:', e);
    }
    return JSON.parse(JSON.stringify(DEFAULT_STATE));
  }
};

window.Storage = Storage;
