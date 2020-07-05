<template>
  <v-container>
    <v-progress-linear
      v-if="$store.state.progress ==true"
      class="mt-10"
      indeterminate
      color="light-blue"
      height="10"
      value="10"
      striped
    ></v-progress-linear>
    <CsvComponent v-if="$store.state.file_type=='csv' && $store.state.progress==false"></CsvComponent>
    <HTMLComponent v-if="$store.state.file_type=='html' && $store.state.progress==false"></HTMLComponent>
    <TexteComponent v-if="$store.state.file_type=='text' && $store.state.progress==false"></TexteComponent>
  </v-container>
</template>
<script>
import CsvComponent from "./preprocess/CsvComponent";
import HTMLComponent from "./preprocess/HTMLComponent";
import TexteComponent from "./preprocess/TexteComponent";

export default {
  components: { CsvComponent, HTMLComponent, TexteComponent },
  props: ["clickedNext", "currentStep"],
  data() {
    return {};
  },
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
    },
    clickedNext(val) {
      console.log("next", val);
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