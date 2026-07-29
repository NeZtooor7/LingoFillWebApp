const languageManager = new window.LingoFillLanguageManager({
  i18nextInstance: window.i18next,
  backendPlugin: window.i18nextHttpBackend,
  localesBaseUrl: window.LINGOFILL_LOCALES_URL
});

async function changeLanguage(language) {
  return languageManager.changeLanguage(language);
}

/*
 * Compatibility with multiselect.js,
 * loading_overlay.js, learning_language.js,
 * and other existing scripts.
 */
window.getCurrentTranslation = (key) => languageManager.translate(key);

window.LingoFillI18n = Object.freeze({
  changeLanguage,
  translate(key) {
    return languageManager.translate(key);
  },
  getCurrentLanguage() {
    return languageManager.getCurrentLanguage();
  }
});

languageManager.initialize();