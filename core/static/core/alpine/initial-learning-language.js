document.addEventListener('alpine:init', () => {
  Alpine.data('initialLearningLanguageDialog', () => ({
    menuOpen: false,
    selectedId: '',
    selectedCode: '',
    selectedLabel: '',
    selectedFlag: '',

    toggleMenu() {
      this.menuOpen = !this.menuOpen;
    },

    closeMenu() {
      this.menuOpen = false;
    },

    persistSelection() {
      if (!this.selectedCode) {
        return;
      }

      try {
        localStorage.setItem('learningLanguage', this.selectedCode);
      } catch (error) {
        console.warn('The default exercise language could not be saved.', error);
      }
    },

    selectOption(option) {
      if (!option) {
        return;
      }

      this.selectedId = option.dataset.languageId;
      this.selectedCode = option.dataset.lang;
      this.selectedLabel = option.dataset.label;
      this.selectedFlag = option.dataset.flag;
      this.closeMenu();
    }
  }));
});