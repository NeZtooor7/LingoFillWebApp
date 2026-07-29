class LingoFillLanguageManager {
  static DEFAULT_LANGUAGE = 'en';
  static STORAGE_KEY = 'language';
  static SUPPORTED_LANGUAGES = Object.freeze(['es', 'en', 'de', 'ja', 'hi', 'ro', 'it', 'pt']);

  constructor({i18nextInstance, backendPlugin, localesBaseUrl}) {
    if (!i18nextInstance) {
      throw new Error('LingoFillLanguageManager requires i18next.');
    }

    if (!backendPlugin) {
      throw new Error('LingoFillLanguageManager requires i18nextHttpBackend.');
    }

    this.i18next = i18nextInstance;
    this.backendPlugin = backendPlugin;
    this.localesBaseUrl = this.normalizeBaseUrl(localesBaseUrl);
    this.languageToggle = document.getElementById('language-toggle');
    this.languageMenu = document.getElementById('language-menu');
    this.selectedLanguageFlag = document.getElementById('selected-language-flag');
    this.selectedLanguageLabel = document.getElementById('selected-language-label');
    this.languageOptions = document.querySelectorAll('.language-option');
  }

  normalizeBaseUrl(baseUrl) {
    const resolvedBaseUrl = baseUrl || '/static/exercises/locales/';

    return resolvedBaseUrl.endsWith('/') ? resolvedBaseUrl : `${resolvedBaseUrl}/`;
  }

  normalizeLanguage(language) {
    return LingoFillLanguageManager
      .SUPPORTED_LANGUAGES
      .includes(language) ?
      language :
      LingoFillLanguageManager.DEFAULT_LANGUAGE;
  }

  getSavedLanguage() {
    try {
      const savedLanguage = localStorage.getItem(
        LingoFillLanguageManager.STORAGE_KEY
      );

      return this.normalizeLanguage(savedLanguage);
    } catch (error) {
      console.warn(
        'The saved interface language could not be read.',
        error
      );

      return LingoFillLanguageManager.DEFAULT_LANGUAGE;
    }
  }

  saveLanguage(language) {
    try {
      localStorage.setItem(LingoFillLanguageManager.STORAGE_KEY, language);
    } catch (error) {
      console.warn('The interface language could not be saved.', error);
    }
  }

  getCurrentLanguage() {
    return (
      this.i18next.resolvedLanguage ||
      this.i18next.language ||
      LingoFillLanguageManager.DEFAULT_LANGUAGE
    );
  }

  translate(key) {
    return this.i18next.isInitialized ? this.i18next.t(key) : key;
  }

  translatePage() {
    document.querySelectorAll('[data-i18n]')
      .forEach((element) => {
        element.textContent = this.translate(
          element.dataset.i18n
        );
      });
    document.querySelectorAll('[data-i18n-placeholder]')
      .forEach((element) => {
        element.placeholder = this.translate(
          element.dataset.i18nPlaceholder
        );
      });
  }

  updateSelectedLanguageUI(language) {
    const selectedOption = document.querySelector(`.language-option[data-lang="${language}"]`);

    if (!selectedOption || !this.selectedLanguageFlag || !this.selectedLanguageLabel) {
      return;
    }

    this.selectedLanguageFlag.src = selectedOption.dataset.flag;
    this.selectedLanguageFlag.alt = selectedOption.dataset.label;
    this.selectedLanguageLabel.textContent = selectedOption.dataset.label;
  }

  setLanguageSelectorBusy(isBusy) {
    if (!this.languageToggle) {
      return;
    }

    this.languageToggle.disabled = isBusy;
    this.languageToggle.toggleAttribute('aria-busy',isBusy);
  }

  openLanguageMenu() {
    if (!this.languageMenu || !this.languageToggle) {
      return;
    }

    this.languageMenu.classList.remove('hidden');
    this.languageToggle.setAttribute('aria-expanded', 'true');
  }

  closeLanguageMenu() {
    if (!this.languageMenu || !this.languageToggle) {
      return;
    }

    this.languageMenu.classList.add('hidden');
    this.languageToggle.setAttribute('aria-expanded', 'false');
  }

  dispatchLanguageChanged(language) {
    document.dispatchEvent(
      new CustomEvent('lingofill:language-changed', {
        detail: { language }
      })
    );
  }

  async changeLanguage(language) {
      const supportedLanguage = this.normalizeLanguage(language);
      this.setLanguageSelectorBusy(true);

      try {
        await this.i18next.changeLanguage(supportedLanguage);
        const resolvedLanguage = this.getCurrentLanguage();
        this.saveLanguage(resolvedLanguage);
        document.documentElement.lang = resolvedLanguage;
        this.translatePage();
        this.updateSelectedLanguageUI(resolvedLanguage);
        this.dispatchLanguageChanged(resolvedLanguage);

        return true;
      } catch (error) {
        console.error(`Could not change the language to ${supportedLanguage}.`, error);

        return false;
      } finally {
        this.setLanguageSelectorBusy(false);
      }
  }

  bindEvents() {
    this.languageToggle?.addEventListener(
      'click',
      (event) => {
        event.stopPropagation();

        if (this.languageMenu?.classList.contains('hidden')) {
          this.openLanguageMenu();
        } else {
          this.closeLanguageMenu();
        }
      }
    );

    this.languageOptions.forEach((option) => {
      option.addEventListener(
        'click',
        async (event) => {
          event.stopPropagation();
          this.closeLanguageMenu();
          await this.changeLanguage(option.dataset.lang);
        }
      );
    });

    document.addEventListener(
      'click',
      (event) => {
        if (!event.target.closest('.language-dropdown')) {
          this.closeLanguageMenu();
        }
      }
    );

    document.addEventListener(
      'keydown',
      (event) => {
        if (event.key === 'Escape') {
          this.closeLanguageMenu();
        }
      }
    );
  }

  async initialize() {
    this.setLanguageSelectorBusy(true);

    try {
      await this.i18next
        .use(this.backendPlugin)
        .init({
          lng: this.getSavedLanguage(),
          fallbackLng: LingoFillLanguageManager.DEFAULT_LANGUAGE,
          supportedLngs: LingoFillLanguageManager.SUPPORTED_LANGUAGES,

          /*
           * Prevents requests such as en-US.json.
           */
          load: 'languageOnly',
          ns: ['translation'],
          defaultNS: 'translation',
          backend: {
            loadPath: `${this.localesBaseUrl}` + '{{lng}}.json'
          },

          interpolation: {
            escapeValue: false
          },

          debug: false
        });

      const language = this.getCurrentLanguage();
      document.documentElement.lang = language;
      this.translatePage();
      this.updateSelectedLanguageUI(language);
      this.dispatchLanguageChanged(language);
      this.bindEvents();

      return true;
    } catch (error) {
      console.error('LingoFill translations could not be initialized.', error);

      return false;
    } finally {
      this.setLanguageSelectorBusy(false);
    }
  }
}

/*
 * Makes the class available to i18n.js.
 */
window.LingoFillLanguageManager = LingoFillLanguageManager;