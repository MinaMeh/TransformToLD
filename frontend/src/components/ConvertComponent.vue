<template>
  <v-container class="mt-10">
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
  </v-container>
</template>
<script>
import CsvComponent from "./convert/CsvComponent.vue";
import HTMLComponent from "./convert/HTMLComponent.vue";
import TextComponent from "./convert/TextComponent.vue";

export default {
  props: ["clickedNext", "currentStep"],
  components: { CsvComponent, HTMLComponent, TextComponent },
  computed: {
    complexFile() {
      return (
        this.$store.state.file_type == "html" ||
        this.$store.state.file_type == "pdf" ||
        this.$store.state.file_type == "image"
      );
    },
  },

  data() {
    return {
      continue: true,
    };
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
    clickedNext(val) {
      console.log("test");
      console.log(val);
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
