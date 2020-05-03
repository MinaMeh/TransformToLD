<template>
  <div>
    <v-progress-linear
      v-if="progress"
      class="mt-10"
      indeterminate
      color="light-blue"
      height="10"
      value="10"
      striped
    ></v-progress-linear>

    <CsvComponent v-if="csv" :terms="results"></CsvComponent>
    <HTMLComponent v-if="html"></HTMLComponent>
  </div>
</template>
<script>
import CsvComponent from "./explore/CsvComponent.vue";
import HTMLComponent from "./explore/HTMLComponent.vue";

export default {
  components: { CsvComponent, HTMLComponent },
  props: ["clickedNext", "currentStep"],
  data() {
    return {
      csv: false,
      html: false,
      progress: true,
      results: []
    };
  },
  computed: {
    type() {
      return this.$store.state.file_content.type;
    },
    terms() {
      return this.$store.state.csv.terms;
    }
  },
  watch: {
    type(newCount, oldCount) {
      console.log("old " + oldCount + " new count " + newCount);
      var type = this.$store.state.file_content.type;
      switch (type) {
        case "csv":
          this.csv = true;
          break;
        case "html":
          this.html = true;
          break;
      }
    },
    terms(newTerms, oldTerms) {
      this.progress = false;

      console.log("old terms " + oldTerms + "new terms " + newTerms);
      this.results = this.$store.state.csv.terms;
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
    var type = this.$store.state.file_content.type;
    switch (type) {
      case "csv":
        this.csv = true;
        break;
      case "html":
        this.html = true;
        break;
    }
    if (!this.continue) {
      this.$emit("can-continue", { value: true });
    } else {
      this.$emit("can-continue", { value: false });
    }
  }
};
</script>
