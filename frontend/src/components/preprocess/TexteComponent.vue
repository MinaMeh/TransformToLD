<template>
  <Paragraphs :sentences="results"></Paragraphs>
</template>
<script>
import Paragraphs from "@/Subcomponents/Paragraphs";
export default {
  components: {
    Paragraphs
  },
  data() {
    return {
      results: null,
      queries: ["text"]
    };
  },
  watch: {
    type(newType, oldType) {
      console.log("old " + oldType + " new type " + newType);
      this.results = this.$store.state.file_content.results;
      console.log("queries" + this.queries);
      console.log(this.results.entities);
      //this.queries = this.results.entities;
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
  computed: {
    type() {
      return this.$store.state.file_content.type;
    }
  },
  mounted() {
    this.results = this.$store.state.file_content.results;
    for (var word in this.results.entities) {
      this.queries.push(this.results.entities[word].name);
    }

    if (this.continue) {
      this.$emit("can-continue", { value: true });
    } else {
      this.$emit("can-continue", { value: false });
    }
  }
};
</script>