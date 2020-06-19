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
    <v-sheet v-if="$store.state.progress" color="grey lighten-4" class="px-3 pt-3 pb-3">
      <v-skeleton-loader class="mx-auto" type="table-tbody"></v-skeleton-loader>
    </v-sheet>

    <CsvComponent v-if="$store.state.file_type=='csv'"></CsvComponent>
    <HTMLComponent v-if="$store.state.file_type=='html'"></HTMLComponent>
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
      continue: true
    };
  },
  computed: {
    filename() {
      return this.$store.state.filename;
    }
  },
  watch: {
    filename(oldName, newName) {
      console.log("oldname" + oldName + "," + "newname" + newName);
      this.progress = false;
    },
    $v: {
      handler: function(val) {
        if (!val.$invalid) {
          this.$emit("can-continue", { value: true });
        } else {
          this.$emit("can-continue", { value: false });
        }
      },
      deep: true
    }
  },
  mounted() {
    if (this.continue) {
      this.$emit("can-continue", { value: true });
    } else {
      this.$emit("can-continue", { value: false });
    }
  }
};
</script>
