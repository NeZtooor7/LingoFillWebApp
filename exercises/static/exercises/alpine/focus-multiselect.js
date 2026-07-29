document.addEventListener('alpine:init', () => {
  Alpine.data('focusMultiselect', () => ({
    open: false,
    selectionVersion: 0,
    translationVersion: 0,

    init() {
      document.addEventListener(
        'languageChanged',
        () => {
          this.translationVersion++;
        }
      );
    },

    toggle() {
      this.open = !this.open;
    },

    close() {
      this.open = false;
    },

    refreshSelection() {
      this.selectionVersion++;
    },

    get selectedItems() {
      /*
       * These reactive values ensure Alpine recalculates
       * the pills after a checkbox or language changes.
       */
      this.selectionVersion;
      this.translationVersion;

      if (!this.$refs.menu) {
        return [];
      }

      const selectedInputs = this.$refs.menu.querySelectorAll('input[type="checkbox"]:checked');

      return Array.from(selectedInputs)
        .map((input) => ({
          value: input.value,
          label: this.getLabel(input)
        }));
    },

    getLabel(input) {
      const key = input.dataset.labelKey;
      const translatedLabel = window.getCurrentTranslation?.(key);

      if (translatedLabel && translatedLabel !== key) {
        return translatedLabel;
      }

      const labelElement = input.closest('.multiselect-option')?.querySelector('[data-i18n]');

      return labelElement?.textContent.trim() || key;
    },

    remove(value) {
      const input = this.$refs.menu?.querySelector(`input[value="${CSS.escape(value)}"]`);

      if (!input) {
        return;
      }

      input.checked = false;
      this.refreshSelection();
    }
  }));
});