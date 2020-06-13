<template>
  <div>
    <v-progress-linear
      v-if="$store.state.progress"
      class="mt-10"
      indeterminate
      color="light-blue"
      height="10"
      value="10"
      striped
    ></v-progress-linear>

    <CsvComponent v-if="$store.state.file_type=='csv'"></CsvComponent>
    <HTMLComponent v-if="$store.state.file_type=='html'"></HTMLComponent>
    <TextComponent v-if="$store.state.file_type=='text'"></TextComponent>
  </div>
</template>
<script>
import CsvComponent from "./explore/CsvComponent.vue";
import HTMLComponent from "./explore/HTMLComponent.vue";
import TextComponent from "./explore/TextComponent.vue";

export default {
  components: { CsvComponent, HTMLComponent, TextComponent },
  props: ["clickedNext", "currentStep"],
  data() {
    return {
      progress: true
    };
  },
  computed: {},
  watch: {
    $v: {
      handler: function() {
        if (this.continue) {
          this.$emit("can-continue", { value: true });
        } else {
          this.$emit("can-continue", { value: false });
        }
      },
      deep: true
    }
  },
  mounted() {
    if (!this.continue) {
      this.$emit("can-continue", { value: true });
    } else {
      this.$emit("can-continue", { value: false });
    }
  }
};
</script>
