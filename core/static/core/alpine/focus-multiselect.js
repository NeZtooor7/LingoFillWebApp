document.addEventListener('alpine:init', () => {
  Alpine.data('focusMultiselect', () => ({
    open: false,
    selectionVersion: 0,
    translationVersion: 0,
    saveError: false,

    init() {
      const preferences = this.$store.exercisePreferences;
      preferences.configure(this.$root.closest('form'));
      const saved = preferences.values.focus;
      const inputs = [...this.$el.querySelectorAll('input[type="checkbox"]')];
      if (!preferences.preserveSubmitted && Array.isArray(saved)) {
        inputs.forEach(input => { input.checked = saved.includes(input.value); });
      }
      preferences.values.focus = inputs.filter(input => input.checked).map(input => input.value);
      this.$nextTick(() => this.selectionVersion++);
      document.addEventListener(
        'lingofill:language-changed',
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
      const selected = [...this.$refs.menu.querySelectorAll('input[type="checkbox"]:checked')]
        .map(input => input.value);
      this.saveError = !this.$store.exercisePreferences.save('focus', selected);
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
