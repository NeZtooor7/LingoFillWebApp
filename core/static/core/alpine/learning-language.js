document.addEventListener('alpine:init', () => {
  Alpine.data('learningLanguageSelector', () => ({
    open: false,
    saving: false,
    saveError: false,

    selected: {language: 'en', label: 'English', flag: ''},

    init() {
      const initialLanguage = this.$el.dataset.initialLanguage || 'en';
      const forceInitialLanguage = Boolean(this.$el.dataset.saveUrl)
        || this.$el.dataset.forceInitialLanguage === 'true';
      let selectedLanguage = initialLanguage;

      if (!forceInitialLanguage) {
        try {
          selectedLanguage = localStorage.getItem('learningLanguage') || initialLanguage;
        } catch (error) {
          console.warn('The saved exercise language could not be read.', error);
        }
      }

      const selectedOption = this.$el.querySelector(`.learning-language-option[data-lang="${initialLanguage}"]`);
      const savedOption = this.$el.querySelector(`.learning-language-option[data-lang="${selectedLanguage}"]`);
      const optionToSelect = forceInitialLanguage ? selectedOption : (savedOption || selectedOption);
      this.selectOption(optionToSelect, false);
      if (forceInitialLanguage) {
        this.rememberSelection();
      }
      this.updateSpokenLanguage();
      document.addEventListener('lingofill:language-changed', (event) => this.updateSpokenLanguage(event.detail?.language));
    },

    toggle() {
      this.open = !this.open;
    },

    close() {
      this.open = false;
    },

    async selectOption(option, save = true) {
      if (!option) {
        return;
      }

      if (this.saving) {
        return;
      }

      const selection = {language: option.dataset.lang, label: option.dataset.label, flag: option.dataset.flag};
      this.close();

      // Initialization must never issue a preference update.
      if (!save) {
        this.selected = selection;
        return;
      }

      this.saving = true;
      this.saveError = false;

      try {
        await this.$store.languagePreferences.save(this.$root.dataset.saveUrl, selection.language);
        this.selected = selection;

        this.rememberSelection();
      } catch (error) {
        this.saveError = true;
      } finally {
        this.saving = false;
      }
    },

    rememberSelection() {
      try {
        localStorage.setItem('learningLanguage', this.selected.language);
      } catch (error) {
        console.warn('The exercise language could not be saved.', error);
      }
    },

    updateSpokenLanguage(language = null) {
      const spokenLanguageInput = document.getElementById('spoken-language-input');

      if (!spokenLanguageInput) {
        return;
      }

      spokenLanguageInput.value = language || window.LingoFillI18n?.getCurrentLanguage() || 'en';
    }
  }));
});
