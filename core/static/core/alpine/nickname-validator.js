document.addEventListener('alpine:init', () => {
  Alpine.data('nicknameValidator', () => ({
    showRules: false,

    validateNickname(input) {
      // Short, otherwise valid names are still in progress while typing.
      // The existing HTML and server validators enforce the minimum length.
      this.showRules = input.value.length > 0 && !/^[A-Za-z][A-Za-z0-9]*$/.test(input.value);
    }
  }));
});
