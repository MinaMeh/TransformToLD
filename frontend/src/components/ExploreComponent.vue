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
    <v-sheet v-if="$store.state.progress" color="grey lighten-4" class="px-3 pt-3 pb-3">
      <v-skeleton-loader class="mx-auto" type="table-tbody"></v-skeleton-loader>
    </v-sheet>

    <CsvComponent v-if="$store.state.file_type=='csv' && $store.state.progress==false"></CsvComponent>
    <HTMLComponent v-if="$store.state.file_type=='html' && $store.state.progress==false"></HTMLComponent>
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
