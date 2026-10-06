document.addEventListener('alpine:init', () => {
    Alpine.data('passwordValidator', (passwordOptional = false) => ({
        password: '',
        passwordOptional,
        showPasswordError: false,
        currentLanguage: 'en',

        init() {
            this.currentLanguage = window.LingoFillI18n?.getCurrentLanguage?.() || 'en';
        },

        setLanguage(language) {
            if (!language) {
                return;
            }

            this.currentLanguage = language.split('-')[0];
        },

        get passwordMessage() {
            if (!this.currentLanguage) {
                return '';
            }

            return window.LingoFillI18n?.translate?.('passwordValidationMessage') || 'passwordValidationMessage';
        },

        passwordIsValid() {
            /*
             * Account editing allows the password fields to stay empty.
             */
            if (this.passwordOptional && this.password.length === 0) {
                return true;
            }

            return (this.password.length >= 10 &&
                /\p{Lu}/u.test(this.password) &&
                /\p{Ll}/u.test(this.password) &&
                /\p{N}/u.test(this.password) &&
                /[^\p{L}\p{N}\s]/u.test(this.password));
        },

        validatePassword(event) {
            if (this.passwordIsValid()) {
                this.showPasswordError = false;
                return;
            }

            event.preventDefault();
            this.showPasswordError = true;

            this.$nextTick(() => {
                document.getElementById('password1')?.focus();
            });
        }
    }));
});