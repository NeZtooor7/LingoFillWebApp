document.addEventListener('alpine:init', () => {
  Alpine.store('theme', {
    dark: localStorage.getItem('theme') !== 'light',
    translationVersion: 0,

    init() {
      /*
       * Changing this reactive value forces Alpine
       * to recalculate buttonLabel.
       */
      document.addEventListener('lingofill:language-changed', () => this.translationVersion++);
    },

    get buttonLabel() {
      /*
       * Access the value so Alpine tracks it.
       */
      this.translationVersion;
      const key = this.dark ? 'lightModeButton' : 'darkModeButton';
      const fallback = this.dark ? 'Light mode' : 'Dark mode';
      const translation = window.getCurrentTranslation?.(key);

      return (translation && translation !== key) ? translation : fallback;
    },

    get buttonIcon() {
      return this.dark ? '☀️' : '🌙';
    },

    toggle() {
      this.dark = !this.dark;
      localStorage.setItem('theme', this.dark ? 'dark' : 'light');
    }
  });

  Alpine.store('loading', {
    active: false,
    message: '',

    start(messageKey, fallbackMessage = 'Loading...') {
      const translatedMessage = window.getCurrentTranslation?.(messageKey);

      this.message = (translatedMessage && translatedMessage !== messageKey)
          ? translatedMessage
          : fallbackMessage;

      this.active = true;
      document.body.classList.add('is-loading');
    },

    stop() {
      this.active = false;
      this.message = '';
      document.body.classList.remove('is-loading');
    }
  });
});