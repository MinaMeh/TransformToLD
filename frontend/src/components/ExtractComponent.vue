<template>
  <v-container>
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
    <HTMLComponent v-if="complexFile"></HTMLComponent>
    <TexteComponent v-if="$store.state.file_type=='text'"></TexteComponent>
  </v-container>
</template>
<script>
import CsvComponent from "./extract/CsvComponent";
import HTMLComponent from "./extract/HTMLComponent";
import TexteComponent from "./extract/TexteComponent";

export default {
  components: { CsvComponent, HTMLComponent, TexteComponent },

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
    filename() {
      return this.$store.state.filename;
    },
  },
  watch: {
    filename(oldName, newName) {
      console.log("oldname" + oldName + "," + "newname" + newName);
      this.progress = false;
    },
    $v: {
      handler: function (val) {
        if (!val.$invalid) {
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
