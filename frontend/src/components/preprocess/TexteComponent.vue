<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <h4 class="text-center">Sentences</h4>
        <v-col v-for="(sentence,i) in $store.state.text.paragraph.sentences" :key="i">
          <v-card v-if="sentence.triplets.length!=0">
            <v-card-text>
              <h6>{{sentence.text}}</h6>
              <v-data-table dense :headers="headers" :items="sentence.triplets">
                <template v-slot:item.selected="{ item }">
                  <v-simple-checkbox v-model="item.selected" :value="item.selected"></v-simple-checkbox>
                </template>
              </v-data-table>
            </v-card-text>
          </v-card>
        </v-col>
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