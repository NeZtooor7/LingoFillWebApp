document.addEventListener('alpine:init', () => {
    Alpine.data('exerciseHistory', () => ({
        search: '',
        currentPage: 1,
        itemsPerPage: 20,
        pageSizeMenuOpen: false,

        normalizedSearch() {
            return this.search.trim().toLocaleLowerCase();
        },

        rows() {
            return Array.from(this.$root.querySelectorAll('[data-history-row]'));
        },

        filteredRows() {
            const query = this.normalizedSearch();

            if (!query) {
                return this.rows();
            }

            return this.rows().filter((row) => {
                const searchableText = (row.dataset.searchText || '').toLocaleLowerCase();

                return searchableText.includes(query);
            });
        },

        totalItems() {
            return this.filteredRows().length;
        },

        totalPages() {
            return Math.max(1, Math.ceil(this.totalItems() / this.itemsPerPage));
        },

        firstItemNumber() {
            if (this.totalItems() === 0) {
                return 0;
            }

            return ((this.currentPage - 1) * this.itemsPerPage) + 1;
        },

        lastItemNumber() {
            return Math.min(this.currentPage * this.itemsPerPage, this.totalItems());
        },

        isRowVisible(row) {
            const filteredRows = this.filteredRows();
            const rowIndex = filteredRows.indexOf(row);

            if (rowIndex === -1) {
                return false;
            }

            const firstIndex = (this.currentPage - 1) * this.itemsPerPage;
            const lastIndex = firstIndex + this.itemsPerPage;

            return rowIndex >= firstIndex && rowIndex < lastIndex;
        },

        refresh() {
            if (this.currentPage > this.totalPages()) {
                this.currentPage = this.totalPages();
            }

            this.rows()
                .forEach((row) => {
                    row.hidden = !this.isRowVisible(row);
                });
        },

        searchChanged() {
            this.currentPage = 1;
            this.$nextTick(() => this.refresh());
        },

        setItemsPerPage(value) {
            this.itemsPerPage = value;
            this.currentPage = 1;
            this.pageSizeMenuOpen = false;

            this.$nextTick(() => {
                this.refresh();
            });
        },

        previousPage() {
            if (this.currentPage <= 1) {
                return;
            }

            this.currentPage--;
            this.refresh();
        },

        nextPage() {
            if (this.currentPage >= this.totalPages()) {
                return;
            }

            this.currentPage++;
            this.refresh();
        },

        goToPage(page) {
            if (page < 1 || page > this.totalPages()) {
                return;
            }

            this.currentPage = page;
            this.refresh();
        },

        pageNumbers() {
            return Array.from({length: this.totalPages()}, (_, index) => index + 1);
        },

        init() {
            this.$nextTick(() => {
                this.refresh();
            });
        }
    }));
});