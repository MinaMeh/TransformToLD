<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <h4 class="text-center">Sentences</h4>
        <v-col v-for="(sentence,i) in $store.state.text.paragraph.sentences" :key="i">
          <v-card v-if="sentence.triplets.length!=0">
            <v-card-text>
              <h6>{{sentence.text}}</h6>
              <v-data-table id="relations" dense :headers="headers" :items="sentence.triplets">
                <template v-slot:item.selected="{ item }">
                  <v-simple-checkbox data-v-step="1" v-model="item.selected" :value="item.selected"></v-simple-checkbox>
                </template>
              </v-data-table>
            </v-card-text>
          </v-card>
        </v-col>
      </v-col>
    </v-row>
    <v-tour name="myTour" :steps="steps"></v-tour>
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
      ],
      steps: [
        {
          target: "[data-v-step='1']", // We're using document.querySelector() under the hood
          header: {
            title: "Select relations"
          },
          content: `Select relations that you want to include in the conversion`,
          params: {
            enableScrolling: false,
            placement: "top"
          }
        },
        {
          target: "#relations", // We're using document.querySelector() under the hood
          header: {
            title: "Edit relations"
          },
          content: `Edit relations if they don't satisfy what you need `,
          params: {
            enableScrolling: false,
            placement: "top"
          }
        }
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
    this.$tours["myTour"].start();

    if (this.continue) {
      this.$emit("can-continue", { value: true });
    } else {
      this.$emit("can-continue", { value: false });
    }
  }
};
</script>