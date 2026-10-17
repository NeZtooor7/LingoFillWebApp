document.addEventListener('alpine:init', () => {
  Alpine.data('exercisePreferenceSelector', () => ({
    saved: {},
    saving: false,
    saveError: false,

    init() {
      this.$el.querySelectorAll('select[name]').forEach(select => {
        this.saved[select.name] = select.value;
      });
    },

    async saveOption(select) {
      const option = select.name;
      const previousValue = this.saved[option];
      if (this.saving) {
        select.value = previousValue;
        return;
      }

      const value = select.value;
      this.saving = true;
      this.saveError = false;
      try {
        const result = await this.$store.languagePreferences.saveValues(
          this.$root.dataset.saveUrl, { option, value }
        );
        if (result.option !== option || result.value !== value) {
          throw new Error('The exercise preference response was invalid.');
        }
        this.saved[option] = value;
      } catch (error) {
        select.value = previousValue;
        this.saveError = true;
      } finally {
        this.saving = false;
      }
    }
  }));
});
