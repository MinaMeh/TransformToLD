<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <h4 class="text-center">Sentences</h4>
        <v-expansion-panels>
          <v-expansion-panel v-for="(sentence,i) in $store.state.text.paragraph.sentences" :key="i">
            <v-expansion-panel-header>{{sentence.text}}</v-expansion-panel-header>
            <v-expansion-panel-content>
              <v-data-table :headers="headers" :items="sentence.triplets">
                <template v-slot:item.selected="{ item }">
                  <v-checkbox v-model="item.selected" :value="item.selected"></v-checkbox>
                </template>
              </v-data-table>
            </v-expansion-panel-content>
          </v-expansion-panel>
        </v-expansion-panels>
      </v-col>
    </v-row>
  </v-container>
</template>
<script>
export default {
  components: {},
  data() {
    return {
      headers: [
        { text: "", value: "selected" },
        { text: "Subject", value: "subject" },
        { text: "Predicate", value: "predicate" },
        { text: "Object", value: "object" }
      ]
    };
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