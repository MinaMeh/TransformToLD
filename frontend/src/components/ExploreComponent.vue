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

    <CsvComponent v-if="csv"></CsvComponent>
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
      progress: true
    };
  },
  computed: {
    count() {
      return this.$store.state.properties.length;
    }
  },

  watch: {
    count(newCount, oldCount) {
      console.log("old " + oldCount + " new count " + newCount);
      this.progress = false;
      var type = this.$store.state.properties.type;
      switch (type) {
        case "csv":
          this.csv = true;
          break;
        case "html":
          this.html = true;
          break;
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
    this.csv = this.$store.state.type;
    if (!this.continue) {
      this.$emit("can-continue", { value: true });
    } else {
      this.$emit("can-continue", { value: false });
    }
  }
};
</script>
