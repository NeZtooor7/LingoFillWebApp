document.addEventListener('alpine:init', () => {
  Alpine.store('languagePreferences', {
    pending: 0,

    get saving() {
      return this.pending > 0;
    },

    async save(url, languageCode) {
      // Anonymous interface-language changes remain local to the browser.
      if (!url) {
        return;
      }

      const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]')?.value;
      if (!csrfToken) {
        throw new Error('The language preference request requires a CSRF token.');
      }

      const controller = new AbortController();
      const timeout = setTimeout(() => controller.abort(), 15000);
      this.pending++;

      try {
        const response = await fetch(url, {
          method: 'POST',
          credentials: 'same-origin',
          mode: 'same-origin',
          headers: {
            'X-CSRFToken': csrfToken,
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json'
          },
          body: new URLSearchParams({ language_code: languageCode }),
          signal: controller.signal
        });

        if (!response.ok || response.redirected) {
          throw new Error('The language preference could not be saved.');
        }

        const result = await response.json();
        if (result.language_code !== languageCode) {
          throw new Error('The language preference response was invalid.');
        }
      } finally {
        clearTimeout(timeout);
        this.pending--;
      }
    }
  });

  Alpine.data('interfaceLanguageSelector', () => ({
    saving: false,
    saveError: false,

    async selectLanguage(language) {
      if (this.saving) {
        return;
      }

      this.saving = true;
      this.saveError = false;
      let previousLanguage;

      try {
        await window.LingoFillI18n.ready;
        previousLanguage = window.LingoFillI18n.getCurrentLanguage();
        window.LingoFillI18n.closeLanguageMenu();

        if (!await window.LingoFillI18n.changeLanguage(language)) {
          throw new Error('The interface language could not be changed.');
        }

        await this.$store.languagePreferences.save(this.$root.dataset.saveUrl, language);
        if (this.$root.dataset.saveUrl) {
          document.dispatchEvent(new CustomEvent('lingofill:interface-language-saved', {
            detail: { language }
          }));
        }
      } catch (error) {
        if (previousLanguage) {
          await window.LingoFillI18n.changeLanguage(previousLanguage);
        }
        this.saveError = true;
      } finally {
        this.saving = false;
      }
    }
  }));
});
