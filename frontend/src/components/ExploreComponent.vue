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

    <CsvComponent v-if="$store.state.file_type=='csv' && $store.state.progress==false"></CsvComponent>
    <HTMLComponent v-if="complexFile && $store.state.progress==false"></HTMLComponent>
    <TextComponent v-if="$store.state.file_type=='text' && $store.state.progress==false"></TextComponent>
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
      progress: true,
      continue: true,
    };
  },
  computed: {
    complexFile() {
      return (
        this.$store.state.file_type == "html" ||
        this.$store.state.file_type == "pdf" ||
        this.$store.state.file_type == "image"
      );
    },
  },
  watch: {
    $v: {
      handler: function () {
        if (this.continue) {
          this.$emit("can-continue", { value: true });
        } else {
          this.$emit("can-continue", { value: false });
        }
      },
      deep: true,
    },
  },
  mounted() {
    if (this.continue) {
      this.$emit("can-continue", { value: true });
    } else {
      this.$emit("can-continue", { value: false });
    }
  },
};
</script>
