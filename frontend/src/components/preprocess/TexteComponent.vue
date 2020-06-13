<template>
  <Paragraphs :sentences="$store.state.text.sentences"></Paragraphs>
</template>
<script>
import Paragraphs from "@/Subcomponents/Paragraphs";
export default {
  components: {
    Paragraphs
  },
  data() {
    return {};
  },
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
  computed: {},
  mounted() {
    if (this.continue) {
      this.$emit("can-continue", { value: true });
    } else {
      this.$emit("can-continue", { value: false });
    }
  }
};
</script>