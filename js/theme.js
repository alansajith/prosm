/**
 * js/theme.js
 * Theme controller: dark/light/system mode support with persistence.
 */

const Theme = {
  init() {
    const saved = this.getSavedTheme();
    this.applyTheme(saved);

    // Watch for OS preference changes
    try {
      window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
        const current = this.getSavedTheme();
        if (current === 'auto') {
          this.applyTheme('auto');
        }
      });
    } catch (e) {
      // Older browsers
    }
  },

  getSavedTheme() {
    try {
      const state = window.Storage ? window.Storage.loadState() : null;
      return state?.settings?.theme || 'auto';
    } catch (e) {
      return 'auto';
    }
  },

  setTheme(theme) {
    if (!['auto', 'light', 'dark'].includes(theme)) return;
    try {
      const state = window.Storage.loadState();
      state.settings.theme = theme;
      window.Storage.saveState(state);
    } catch (e) {
      // storage unavailable
    }
    this.applyTheme(theme);
  },

  toggle() {
    const active = this.getActiveTheme();
    // Toggle between light and dark
    const next = active === 'dark' ? 'light' : 'dark';
    this.setTheme(next);
    return next;
  },

  getActiveTheme() {
    const attr = document.documentElement.getAttribute('data-theme');
    if (attr === 'dark') return 'dark';
    if (attr === 'light') return 'light';
    const prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
    return prefersDark ? 'dark' : 'light';
  },

  applyTheme(theme) {
    const root = document.documentElement;
    if (theme === 'dark') {
      root.setAttribute('data-theme', 'dark');
    } else if (theme === 'light') {
      root.setAttribute('data-theme', 'light');
    } else {
      // auto
      root.removeAttribute('data-theme');
    }
    this.updateToggleUi();
  },

  updateToggleUi() {
    const btn = document.getElementById('theme-toggle-btn');
    if (!btn) return;
    const current = this.getActiveTheme();
    const isDark = current === 'dark';
    btn.setAttribute('aria-label', isDark ? 'Switch to light mode' : 'Switch to dark mode');
    btn.innerHTML = isDark
      ? '<span class="theme-icon">☼</span><span class="theme-label">Light</span>'
      : '<span class="theme-icon">☽</span><span class="theme-label">Dark</span>';
  }
};

window.Theme = Theme;
