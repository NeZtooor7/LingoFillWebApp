document.addEventListener('alpine:init', () => {
  Alpine.data('learningLanguageSelector', () => ({
    open: false,

    selected: {language: 'en', label: 'English', flag: ''},

    init() {
      const initialLanguage = this.$el.dataset.initialLanguage || 'en';
      const forceInitialLanguage = this.$el.dataset.forceInitialLanguage === 'true';
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
      this.selectOption(optionToSelect, forceInitialLanguage);
      this.updateSpokenLanguage();
      document.addEventListener('lingofill:language-changed', (event) => this.updateSpokenLanguage(event.detail?.language));
    },

    toggle() {
      this.open = !this.open;
    },

    close() {
      this.open = false;
    },

    selectOption(option, save = true) {
      if (!option) {
        return;
      }

      this.selected = {language: option.dataset.lang, label: option.dataset.label, flag: option.dataset.flag};

      if (save) {
        try {
          localStorage.setItem('learningLanguage', this.selected.language);
        } catch (error) {
          console.warn('The exercise language could not be saved.', error);
        }
      }

      this.close();
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