document.addEventListener('alpine:init', () => {
  Alpine.data('clipboardExercise', () => ({
    canCopy: false,
    status: '',

    init() {
      this.updateState();
    },

    translate(key, fallback) {
      const translation = window.getCurrentTranslation?.(key);

      return (translation &&translation !== key) ? translation : fallback;
    },

    normalizeSpaces(text) {
      return text.replace(/\s+/g, ' ').trim();
    },

    updateState() {
      const blankInputs = this.$root.querySelectorAll('.blank-input');

      this.canCopy =
        blankInputs.length > 0 &&
        Array.from(blankInputs)
          .every((input) => input.value.trim() !== '');

      if (!this.canCopy) {
        this.status = '';
      }
    },

    buildCompletedSentence(row) {
      const number = row.dataset.number;
      let sentence = '';

      row.childNodes.forEach((node) => {
        if (node.nodeType !== Node.ELEMENT_NODE) {
          return;
        }

        if (node.classList.contains('sentence-number')) {
          return;
        }

        if (node.classList.contains('sentence-part')) {
          sentence += node.textContent;
          return;
        }

        if (node.classList.contains('blank-input')) {
          sentence += node.value.trim();
        }
      });

      return (`${number}. ` + this.normalizeSpaces(sentence));
    },

    copyWithTemporaryTextarea(text) {
      const textarea = document.createElement('textarea');
      textarea.value = text;
      textarea.style.position = 'fixed';
      textarea.style.top = '0';
      textarea.style.left = '0';
      textarea.style.width = '1px';
      textarea.style.height = '1px';
      textarea.style.padding = '0';
      textarea.style.border = '0';
      textarea.style.opacity = '0';
      document.body.appendChild(textarea);
      textarea.focus();
      textarea.select();
      textarea.setSelectionRange(0, textarea.value.length);
      const copied = document.execCommand('copy');
      textarea.remove();

      if (!copied) {
        throw new Error('Fallback clipboard copy failed.');
      }
    },

    async writeToClipboard(text) {
      /*
       * Try the modern Clipboard API first.
       */
      if (navigator.clipboard?.writeText) {
        try {
          await navigator.clipboard.writeText(text);
          return;
        } catch (error) {
          console.warn('Modern Clipboard API failed. Trying fallback copy.', error);
        }
      }

      /*
       * Used for HTTP LAN addresses or when browser
       * clipboard permission is rejected.
       */
      this.copyWithTemporaryTextarea(text);
    },

    async copyCompletedSentences() {
      this.status = '';
      const rows = this.$root.querySelectorAll('.sentence-row');

      if (rows.length === 0) {
        console.error('No .sentence-row elements were found.');
        this.status = 'No sentences were found to copy.';

        return;
      }

      const finalText = Array.from(rows)
        .map((row) => this.buildCompletedSentence(row))
        .join('\n');
      console.log('LingoFill text prepared for copying:', finalText);

      try {
        await this.writeToClipboard(finalText);

        this.status = this.translate('copiedMessage', 'Copied to clipboard.');
      } catch (error) {
        console.error('Clipboard copy failed.', error);

        this.status = 'Clipboard copy failed. Please check the browser console.';
      }
    }
  }));
});