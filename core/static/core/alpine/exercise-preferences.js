document.addEventListener('alpine:init', () => {
  Alpine.store('exercisePreferences', {
    configured: false,
    key: '',
    path: '/',
    preserveSubmitted: false,
    values: {},

    configure(form) {
      if (this.configured || !form) {
        return;
      }
      this.configured = true;
      this.key = form.dataset.preferenceKey;
      this.path = form.dataset.preferencePath;
      this.preserveSubmitted = form.dataset.optionsBound === 'true';

      try {
        const prefix = `${this.key}=`;
        const cookie = document.cookie.split(';').map(part => part.trim())
          .find(part => part.startsWith(prefix));
        if (!cookie) {
          return;
        }
        const saved = JSON.parse(decodeURIComponent(cookie.slice(prefix.length)));
        if (!saved || typeof saved !== 'object' || Array.isArray(saved)) {
          return;
        }
        for (const name of ['level', 'sentence_count', 'blank_count']) {
          if (typeof saved[name] === 'string' && saved[name].length <= 10) {
            this.values[name] = saved[name];
          }
        }
        if (Array.isArray(saved.focus)) {
          this.values.focus = [...new Set(saved.focus.filter(value => typeof value === 'string'
            && value.length <= 20))].slice(0, 5);
        }
      } catch (error) {
        console.warn('Saved exercise options could not be read.', error);
      }
    },

    save(name, value) {
      this.values[name] = value;
      if (!this.key) {
        return false;
      }
      try {
        const encoded = encodeURIComponent(JSON.stringify(this.values));
        const secure = window.location.protocol === 'https:' ? '; Secure' : '';
        document.cookie = `${this.key}=${encoded}; Max-Age=31536000; Path=${this.path}; SameSite=Lax${secure}`;
        return document.cookie.split(';').some(part => part.trim() === `${this.key}=${encoded}`);
      } catch (error) {
        console.warn('Exercise options could not be saved in this browser.', error);
        return false;
      }
    }
  });

  Alpine.data('exercisePreferenceSelector', () => ({
    saveError: false,

    init() {
      const preferences = this.$store.exercisePreferences;
      preferences.configure(this.$root.closest('form'));
      this.$el.querySelectorAll('select[name]').forEach(select => {
        const saved = preferences.values[select.name];
        if (!preferences.preserveSubmitted && [...select.options].some(option => option.value === saved)) {
          select.value = saved;
        }
        preferences.values[select.name] = select.value;
      });
    },

    saveOption(select) {
      this.saveError = !this.$store.exercisePreferences.save(select.name, select.value);
    }
  }));
});
