<script>
export default { 
  props: ["url", "postData", "message", "btnClass", "btnText"],
  created() {
    this.dataToSend = this.postData;
  },
  data() {
    return {
      dataToSend: null,
      modalState: false,
    };
  },
  methods: {
    handleCloseButton() {
      this.modalState = false;
      window.eventBus.$emit("closed-modal-popup");
    },
    handleActionButton() {
      this.modalState = true;
    },
    handleConfirmButton() {
      this.$http.post(this.url, this.dataToSend).then(() => {
        this.$emit("onConfirm");
        this.handleCloseButton();
      });
    },
  },
};
</script>

<template>
  <div class="ConfirmModalWrapper">
    <button
      class="btn btn-xs"
      @click="handleActionButton"
      v-bind:class="btnClass"
    >
      <div v-html="btnText"></div>
    </button>
    <div class="modal" v-bind:class="{ 'is-active': modalState }">
      <div class="modal-background"></div>
      <div class="modal-content">
        <h4>{{ message }}</h4>
        <button class="btn btn-success" @click="handleConfirmButton">Ok</button>
        <button class="btn btn-warning" @click="handleCloseButton">
          Cancel
        </button>
      </div>
      <button class="modal-close" @click="handleCloseButton"></button>
    </div>
  </div>
</template>