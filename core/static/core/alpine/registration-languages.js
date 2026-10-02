document.addEventListener("alpine:init", () => {

    Alpine.data("registrationInterfaceLanguageSelector", () => ({
        open: false,

        selectedId: "",
        selectedLabel: "",
        selectedFlag: "",

        init() {
            const initialId = String(
                this.$root.dataset.initialLanguageId || ""
            );

            const options = [
                ...this.$root.querySelectorAll(
                    ".registration-interface-language-option"
                )
            ];

            let selectedOption = options.find(
                option => option.dataset.languageId === initialId
            );

            if (!selectedOption) {
                selectedOption = options[0];
            }

            if (selectedOption) {
                this.setSelected(selectedOption);
            }
        },

        toggle() {
            this.open = !this.open;
        },

        close() {
            this.open = false;
        },

        setSelected(option) {
            this.selectedId = option.dataset.languageId;
            this.selectedLabel = option.dataset.label;
            this.selectedFlag = option.dataset.flag;
        },

        selectOption(option) {
            this.setSelected(option);
            this.close();
        },
    }));


    Alpine.data("registrationLearningLanguagesMultiselect", () => ({
        open: false,
        selectedItems: [],

        init() {
            this.refreshSelection();
        },

        toggle() {
            this.open = !this.open;
        },

        close() {
            this.open = false;
        },

        refreshSelection() {
            const checked = [
                ...this.$root.querySelectorAll(
                    'input[name="learning_languages"]:checked'
                )
            ];

            this.selectedItems = checked.map(input => ({
                value: input.value,
                label: input.dataset.label,
                flag: input.dataset.flag,
            }));
        },

        remove(value) {
            const input = this.$root.querySelector(
                `input[name="learning_languages"][value="${value}"]`
            );

            if (!input) {
                return;
            }

            input.checked = false;
            this.refreshSelection();
        },
    }));

});