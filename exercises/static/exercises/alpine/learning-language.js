document.addEventListener('alpine:init', () => {
  Alpine.data('learningLanguageSelector', () => ({
    open: false,

    selected: {language: 'de', label: 'Deutsch', flag: ''},

    init() {
      let savedLanguage = 'de';

      try {
        savedLanguage = localStorage.getItem('learningLanguage') || 'de';
      } catch (error) {
        console.warn('The saved exercise language could not be read.', error);
      }

      const savedOption = this.$el.querySelector(`.learning-language-option[data-lang="${savedLanguage}"]`);
      const fallbackOption = this.$el.querySelector('.learning-language-option[data-lang="de"]');
      this.selectOption(savedOption || fallbackOption, false);
      this.updateSpokenLanguage();
      document.addEventListener('languageChanged', (event) => this.updateSpokenLanguage(event.detail?.language));
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