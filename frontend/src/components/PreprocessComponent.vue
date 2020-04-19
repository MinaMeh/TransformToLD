<template>
  <v-container>
    <v-progress-linear
      v-if="progress"
      class="mt-10"
      indeterminate
      color="light-blue"
      height="10"
      value="10"
      striped
    ></v-progress-linear>
    <v-sheet v-if="progress" color="grey lighten-4" class="px-3 pt-3 pb-3">
      <v-skeleton-loader class="mx-auto" type="table-tbody"></v-skeleton-loader>
    </v-sheet>

    <CsvComponent v-if="csv"></CsvComponent>
    <HTMLComponent v-if="html"></HTMLComponent>
    <TexteComponent v-if="texte"></TexteComponent>
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
    return {
      csv: false,
      html: false,
      texte: false,
      progress: true
    };
  },
  computed: {
    type() {
      return this.$store.state.file_content.type;
    }
  },

  watch: {
    type(newType, oldType) {
      console.log("old " + oldType + " new count " + newType);
      this.progress = false;
      var type = this.$store.state.file_content.type;
      switch (type) {
        case "csv":
          this.csv = true;
          this.html = false;
          this.progress = false;
          break;
        case "html":
          this.html = true;
          this.csv = false;
          this.progress = false;
          break;
        case "text":
          this.texte = true;
      }
    },

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