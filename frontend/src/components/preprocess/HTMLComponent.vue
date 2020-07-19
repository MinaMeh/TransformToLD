<template>
  <v-container>
    <v-tabs class="mt-8" v-model="tab">
      <v-tab id="tables">Tables</v-tab>
      <v-tab id="paragraphs">Paragraphs</v-tab>
    </v-tabs>
    <v-tabs-items v-model="tab">
      <v-tab-item>
        <v-col cols="12">
          <v-card v-for="table in tables_selected" :key="table.id" class="mt-3">
            <v-card-title>
              <h2 class="table_id">Table #{{table.id}}</h2>
            </v-card-title>
            <v-card-text>
              <v-col col="9">
                <v-simple-table dense class="mt-5">
                  <thead>
                    <tr>
                      <th>Column</th>
                      <th>Translation</th>
                      <th>Combinaisons</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="header in tables_headers(table)" :key="header.name">
                      <td>{{header.name}}</td>
                      <td>{{header.translated}}</td>
                      <td>
                        <v-chip
                          v-for="comb in header.combinaison"
                          :key="comb"
                          class="primary ma-2"
                        >{{comb}}</v-chip>
                      </td>
                    </tr>
                  </tbody>
                </v-simple-table>
              </v-col>
            </v-card-text>
          </v-card>
        </v-col>
      </v-tab-item>
      <v-tab-item>
        <v-col cols="12" v-for="(paragraph,index) in paragraphs_selected" :key="index" class="mt-3">
          <v-card>
            <v-card-title>
              <h2>Paragraph #{{paragraph.id}}</h2>
            </v-card-title>
            <v-card-text>
              <v-row>
                <v-col cols="12">
                  <h4 class="text-center relations">Sentences</h4>
                  <v-col v-for="(sentence,i) in paragraph.sentences" :key="i">
                    <v-card v-if="sentence.triplets.length!=0">
                      <v-card-text>
                        <h6>{{sentence.text}}</h6>
                        <v-data-table dense :headers="headers" :items="sentence.triplets">
                          <template v-slot:item.selected="{ item }">
                            <v-simple-checkbox v-model="item.selected" :value="item.selected"></v-simple-checkbox>
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
                                  <v-text-field
                                    v-model="item.subject"
                                    label="Edit"
                                    single-line
                                    counter
                                  ></v-text-field>
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
                                  <v-text-field
                                    v-model="item.predicate"
                                    label="Edit"
                                    single-line
                                    counter
                                  ></v-text-field>
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
                                  <v-text-field
                                    v-model="item.object"
                                    label="Edit"
                                    single-line
                                    counter
                                  ></v-text-field>
                                </template>
                              </v-edit-dialog>
                            </div>
                          </template>
                        </v-data-table>
                        <v-snackbar v-model="snack" :timeout="3000" :color="snackColor">
                          {{ snackText }}
                          <v-btn text @click="snack = false">Close</v-btn>
                        </v-snackbar>
                      </v-card-text>
                    </v-card>
                  </v-col>
                </v-col>
              </v-row>
            </v-card-text>
          </v-card>
        </v-col>
      </v-tab-item>
    </v-tabs-items>
    <v-tour name="myTour" :steps="steps"></v-tour>
  </v-container>
</template>
<script>
export default {
  name: "HTMLComponent",
  components: {},
  data() {
    return {
      tab: null,
      continue: true,
      selected: "",
      headers: [
        { text: "", value: "selected" },
        { text: "Subject", value: "subject" },
        { text: "Predicate", value: "predicate" },
        { text: "Object", value: "object" }
      ],
      steps: [
        {
          target: "#tables", // We're using document.querySelector() under the hood
          header: {
            title: "Confirm tables preprocessing"
          },
          content: `Confirm each table columns preprocessing`,
          params: {
            placement: "right"
          }
        },

        {
          target: "#paragraphs", // We're using document.querySelector() under the hood
          header: {
            title: "Select Paragraphs relations"
          },
          content: `Select relation that you want to include in the conversion `,
          params: {
            placement: "right"
          }
        },
        {
          target: ".relations", // We're using document.querySelector() under the hood
          header: {
            title: "Select relations"
          },
          content: `For each paragraph select relations that you want to include in the conversion`,
          params: {}
        }
      ]
    };
  },
  computed: {
    tables_selected() {
      var selected = [];
      this.$store.state.html.tables.forEach(function(table) {
        if (table.selected) selected.push(table);
      });
      return selected;
    },
    paragraphs_selected() {
      var selected = [];
      this.$store.state.html.paragraphs.forEach(function(paragraph) {
        if (paragraph.selected) selected.push(paragraph);
      });
      return selected;
    }
  },
  methods: {
    tables_headers: function(table) {
      var headers_selected = [];

      table.headers.forEach(function(header) {
        if (header.selected == true) headers_selected.push(header);
      });
      return headers_selected;
    },
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
    this.$tours["myTour"].start();

    if (this.continue) {
      this.$emit("can-continue", { value: true });
    } else {
      this.$emit("can-continue", { value: false });
    }
  }
};
</script>