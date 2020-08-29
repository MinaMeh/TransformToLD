<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <h4 class="text-center">Sentences</h4>
        <v-col v-for="(sentence,i) in $store.state.text.paragraph.sentences" :key="i">
          <v-card v-if="sentence.triplets.length!=0">
            <v-card-text>
              <h6>{{sentence.text}}</h6>
              <v-row>
              <v-col cols="12">
                <h3>Relations</h3>

              <v-data-table id="relations" dense :headers="headers" :items="sentence.triplets">
                <template v-slot:item.selected="{ item }">
                  <v-simple-checkbox data-v-step="1" v-model="item.selected" :value="item.selected"></v-simple-checkbox>
                </template>
                <template v-slot:item.subject="{ item }">
                  <div>
                    <v-edit-dialog
                      :return-value.sync="item.subject"
                      lazy
                      @save="save"
                      @cancel="cancel"
                      @open="open"
                      @close="close"
                    >
                      {{ item.subject }}
                      <template v-slot:input>
                        <v-text-field v-model="item.subject" label="Edit" single-line counter></v-text-field>
                      </template>
                    </v-edit-dialog>
                  </div>
                </template>
                <template v-slot:item.predicate="{ item }">
                  <div>
                    <v-edit-dialog
                      :return-value.sync="item.predicate"
                      lazy
                      @save="save"
                      @cancel="cancel"
                      @open="open"
                      @close="close"
                    >
                      {{ item.predicate }}
                      <template v-slot:input>
                        <v-text-field v-model="item.predicate" label="Edit" single-line counter></v-text-field>
                      </template>
                    </v-edit-dialog>
                  </div>
                </template>
                <template v-slot:item.object="{ item }">
                  <div>
                    <v-edit-dialog
                      :return-value.sync="item.object"
                      lazy
                      @save="save"
                      @cancel="cancel"
                      @open="open"
                      @close="close"
                    >
                      {{ item.object }}
                      <template v-slot:input>
                        <v-text-field v-model="item.object" label="Edit" single-line counter></v-text-field>
                      </template>
                    </v-edit-dialog>
                  </div>
                </template>
              </v-data-table>
              <v-snackbar v-model="snack" :timeout="3000" :color="snackColor">
                {{ snackText }}
                <v-btn text @click="snack = false">Close</v-btn>
              </v-snackbar>
              </v-col>
              <v-divider inset ></v-divider>
              <v-col cols="12">
                <h3>Entities</h3>
                <v-data-table :headers="headersEnt" :items="sentence.entities">
                 <template v-slot:item.selected="{ item }">
                  <v-simple-checkbox v-model="item.selected" :value="item.selected"></v-simple-checkbox>
                </template>

                </v-data-table>
              </v-col>
              </v-row>
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
      snack: false,
      snackColor: "",
      snackText: "",

      headers: [
        { text: "", value: "selected" },
        { text: "Subject", value: "subject" },
        { text: "Predicate", value: "predicate" },
        { text: "Object", value: "object" }
      ],
            headersEnt: [
        { text: "", value: "selected" },
        { text: "Entity", value: "text" },
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
  computed: {
    guide() {
      return this.$store.state.guide;
    }
  },

  watch: {
    guide(newValue) {
      if (newValue == true) this.$tours["myTour"].start();
      else this.$tours["myTour"].stop();
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
  methods: {
    save() {
      this.snack = true;
      this.snackColor = "success";
      this.snackText = "Data saved";
    },
    cancel() {
      this.snack = true;
      this.snackColor = "error";
      this.snackText = "Canceled";
    },
    open() {
      this.snack = true;
      this.snackColor = "info";
      this.snackText = "Edit header name";
    },
    close() {
      console.log("Dialog closed");
    }
  },
  mounted() {
    if (this.$store.state.guide) this.$tours["myTour"].start();

    if (this.continue) {
      this.$emit("can-continue", { value: true });
    } else {
      this.$emit("can-continue", { value: false });
    }
  }
};
</script>