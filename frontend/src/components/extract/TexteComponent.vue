<template>
  <Paragraphs :paragraph="$store.state.text.paragraph" :sentences="$store.state.text.sentences"></Paragraphs>
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
  watch: {},
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
  mounted() {
    if (this.continue) {
      this.$emit("can-continue", { value: true });
    } else {
      this.$emit("can-continue", { value: false });
    }
  }
};
</script>