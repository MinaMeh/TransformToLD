<template>
  <v-container>
    <v-row>
      <v-col cols="12" class="mt-8">
        <v-card>
          <v-card-title>
            <h2>File Statistics</h2>
          </v-card-title>
          <v-card-text>
            <v-col cols="5">
              <v-simple-table>
                <tr>
                  <th>File size</th>
                  <td>{{ $store.state.size }}</td>
                </tr>
                <tr>
                  <th>Number of tables</th>
                  <td>{{ $store.state.html.num_tables }}</td>
                </tr>
                <tr>
                  <th>Number of paragraphs</th>
                  <td>{{ $store.state.html.num_paragraphs }}</td>
                </tr>
              </v-simple-table>
            </v-col>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    <v-tabs class="mt-8" v-model="tab">
      <v-tab id="tables">Tables</v-tab>
      <v-tab id="paragraphs">Paragraphs</v-tab>
    </v-tabs>
    <v-tabs-items v-model="tab">
      <v-tab-item>
        <v-col cols="12">
          <v-card v-for="table in $store.state.html.tables" :key="table.id" class="mt-3">
            <v-card-title>
              <v-checkbox v-model="table.selected" :id="String(table.id)" class="mt-10"></v-checkbox>
              <h2 class="table_id">Table #{{ table.id }}</h2>
            </v-card-title>
            <v-card-text>
              <v-col cols="6">
                <h3>Table Statistics</h3>
                <v-simple-table dense>
                  <tr>
                    <th>Number of lines</th>
                    <td>{{ table.lines }}</td>
                  </tr>
                  <tr>
                    <th>Number of columns</th>
                    <td>{{ table.columns }}</td>
                  </tr>
                </v-simple-table>
              </v-col>
              <v-col col="12">
                <v-data-table dense class="table_cols" :headers="headers" :items="table.headers">
                  <template v-slot:item="header">
                    <tr>
                      <td>
                        <v-checkbox
                          v-model="header.item.selected"
                          :disabled="!table.selected"
                          :id="String(header.item.name)"
                          :value="header.item.selected"
                        ></v-checkbox>
                      </td>
                      <td>
                        <div class="mt-5 headline">
                          <v-edit-dialog
                            :return-value.sync="header.item.name"
                            lazy
                            @save="save"
                            @cancel="cancel"
                            @open="open"
                            @close="close"
                          >
                            {{ header.item.name }}
                            <template v-slot:input>
                              <v-text-field
                                v-model="header.item.name"
                                label="Edit"
                                single-line
                                counter
                              ></v-text-field>
                            </template>
                          </v-edit-dialog>
                        </div>
                      </td>
                      <td>
                        <v-select :items="datatypes" v-model="header.item.type"></v-select>
                      </td>
                    </tr>
                  </template>
                </v-data-table>
                <v-snackbar v-model="snack" :timeout="3000" :color="snackColor">
                  {{ snackText }}
                  <v-btn text @click="snack = false">Close</v-btn>
                </v-snackbar>
              </v-col>
            </v-card-text>
          </v-card>
        </v-col>
      </v-tab-item>
      <v-tab-item>
        <v-col
          cols="12"
          v-for="paragraph in $store.state.html.paragraphs"
          :key="paragraph.id"
          class="mt-3"
        >
          <v-row>
            <v-col cols="12">
              <v-card>
                <v-card-title>
                  <v-checkbox
                    class="mt-10 paragraph_id"
                    v-model="paragraph.selected"
                    :id="String(paragraph.id)"
                    :value="paragraph.selected"
                  ></v-checkbox>
                  <h2>Paragraph #{{ paragraph.id }}</h2>
                </v-card-title>
                <v-card-text>
                  <v-row>{{ paragraph.paragraph }}</v-row>
                  <v-row>
                    <v-col cols="12">
                      <h4 class="text-center">Sentences</h4>
                      <v-data-table :headers="headersText" :items="paragraph.sentences">
                        <template v-slot:item.id="{item}">#{{paragraph.sentences.indexOf(item)+1}}</template>
                      </v-data-table>
                    </v-col>
                  </v-row>
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>
        </v-col>
      </v-tab-item>
    </v-tabs-items>
    <v-tour name="myTour" :steps="steps"></v-tour>
  </v-container>
</template>
<script>
export default {
  name: "HTMLComponent",
  data() {
    return {
      tab: null,
      continue: true,
      selected: "",
      tables_selected: [],

      snack: false,
      snackColor: "",
      snackText: "",

      headers: [
        { text: "Add", value: "Add" },
        { text: "Header", value: "header", sortable: true },
        { text: "Type", value: "type" }
      ],
      headersText: [
        { text: "id", value: "id" },

        { text: "Sentence", value: "text" }
      ],
      content: null,
      datatypes: [
        "xsd:int",
        "xsd:float",
        "xsd:string",
        "xsd:boolean",
        "xsd:date"
      ],
      steps: [
        {
          target: "#tables", // We're using document.querySelector() under the hood
          header: {
            title: "Select tables"
          },
          content: `Select Tables that you want to include in the conversion`,
          params: {
            placement: "right"
          }
        },
        {
          target: ".table_id", // We're using document.querySelector() under the hood
          header: {
            title: "Select table"
          },
          content: `Select Table `,
          params: {
            enableScrolling: false
          }
        },
        {
          target: ".table_cols", // We're using document.querySelector() under the hood
          header: {
            title: "Select table columns"
          },
          content: `Select table columns that you want to include in the conversion `,
          params: {
            placement: "top"
          }
        },
        {
          target: "#paragraphs", // We're using document.querySelector() under the hood
          header: {
            title: "Select Paragraphs"
          },
          content: `Select paragraphs that you want to include in the conversion `,
          params: {
            placement: "right"
          }
        },
        {
          target: ".paragraph_id", // We're using document.querySelector() under the hood
          header: {
            title: "Select Paragraph"
          },
          content: `Select paragraph`,
          params: {}
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
