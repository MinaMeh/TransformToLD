<template>
  <v-container>
    <v-tabs class="mt-8" v-model="tab">
      <v-tab id="tables">Tables</v-tab>
      <v-tab id="paragraphs">Paragraphs</v-tab>
    </v-tabs>
    <v-tabs-items v-model="tab">
      <v-tab-item>
        <v-row>
          <v-col cols="12" v-for="table in tables_selected" :key="table.id">
            <v-card>
              <v-card-title>
                <h2 class="mt-3">Table #{{table.id }}</h2>
              </v-card-title>
              <v-card-text>
                <SearchClass
                  v-if="modalSearchClass"
                  @close="modalSearchClass = false"
                  :rowClass="$store.state.csv.rowClass"
                  @closeClass="modalSearchClass = false"
                  :active="modalSearchClass"
                  :table="modalData"
                ></SearchClass>
                <CreateClass
                  v-if="modalCreateClass"
                  @close="modalCreateClass = false"
                  @closeClass="updateRowClass"
                  :active="modalCreateClass"
                  :table="modalData"
                ></CreateClass>

                <v-card>
                  <v-card-text>
                    <v-row>
                      <v-col cols="5">
                        <div class="headline mt-4 mr-2">Table rows are of class</div>
                      </v-col>
                      <v-col cols="4">
                        <v-text-field
                          v-if="!table.rowClass"
                          disabled
                          label="Select a class"
                          return-object
                        ></v-text-field>
                        <v-text-field
                          v-if="table.rowClass"
                          disabled
                          :value="table.rowClass.prefixedName"
                          label="Select a class"
                          return-object
                        ></v-text-field>
                      </v-col>
                      <v-col cols="3">
                        <v-tooltip bottom>
                          <template v-slot:activator="{ on, attrs }">
                            <v-btn
                              color="blue"
                              dark
                              class="mx-2 row-class"
                              fab
                              v-bind="attrs"
                              v-on="on"
                              small
                              @click.stop="modalSearchClass = true"
                              @click="openSearchClassModal(table)"
                            >
                              <v-icon dark>mdi-magnify</v-icon>
                            </v-btn>
                          </template>
                          <span>Search a class</span>
                        </v-tooltip>
                        <v-tooltip bottom>
                          <template v-slot:activator="{ on, attrs }">
                            <v-btn
                              color="success"
                              dark
                              class="mx-2"
                              fab
                              v-bind="attrs"
                              v-on="on"
                              small
                              @click.stop="modalCreateClass = true"
                              @click="openCreateClassModal(table)"
                              :table="modalData"
                            >
                              <v-icon dark>mdi-plus</v-icon>
                            </v-btn>
                          </template>
                          <span>Create a class</span>
                        </v-tooltip>
                      </v-col>
                    </v-row>
                    <v-row>
                      <v-col cols="5">
                        <div class="headline mt-3 mr-5">Row ID:</div>
                      </v-col>
                      <v-col cols="4">
                        <v-select
                          class="row-id"
                          v-model="table.rowId"
                          :items="table.terms"
                          label="Select a term"
                          item-value="property"
                          item-text="property"
                          multiple
                          return-object
                        ></v-select>
                      </v-col>
                    </v-row>
                  </v-card-text>
                </v-card>
                <v-row>
                  <v-col class="headers" cols="12" v-for="prop in table.terms" :key="prop.uri">
                    <v-card>
                      <v-card-text>
                        <v-row align="center" justify="center">
                          <div class="headline">{{prop.property}}</div>
                          <v-col cols="8" class="ml-5">
                            <v-select
                              v-model="prop.selected"
                              label="Select a term"
                              :value="prop.selected.uri"
                              :items="prop.result"
                              item-value="uri"
                              :item-text="item => item.prefixedName +' - (score = '+ item.score+' )' +' - (term = '+ item.term+' )'"
                              return-object
                            >
                              <template v-slot:selection="{ item }">
                                <a v-bind:href="item.uri" target="__">{{item.uri}}</a>
                              </template>
                            </v-select>
                          </v-col>
                          <createProp
                            v-if="modalCreate"
                            @close="modalCreate = false"
                            :prop="modalData"
                            :active="modalCreate"
                          ></createProp>
                          <v-tooltip bottom>
                            <template v-slot:activator="{ on, attrs }">
                              <v-btn
                                color="success"
                                dark
                                class="mx-2"
                                fab
                                small
                                v-bind="attrs"
                                v-on="on"
                                @click.stop="modalCreate = true"
                                @click="openCreateModal(prop)"
                              >
                                <v-icon dark>mdi-plus</v-icon>
                              </v-btn>
                            </template>
                            <span>Create a new property</span>
                          </v-tooltip>

                          <Modal
                            v-if="modalVisible"
                            @close="modalVisible = false"
                            :prop="modalData"
                            :active="modalVisible"
                          ></Modal>
                          <v-btn
                            color="blue"
                            dark
                            class="mx-2"
                            fab
                            small
                            @click.stop="modalVisible = true"
                            @click="openModal(prop)"
                          >
                            <v-icon dark>mdi-magnify</v-icon>
                          </v-btn>

                        </v-row>
                      </v-card-text>
                      <v-divider></v-divider>
                    </v-card>
                  </v-col>
                </v-row>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </v-tab-item>
      <v-tab-item>
        <v-row>
          <v-col cols="12" v-for="(paragraph,index) in paragraphs_selected" :key="index">
            <v-card>
              <v-card-title>
                <h2>Paragraph #{{paragraph.id}}</h2>
              </v-card-title>
              <v-card-text>
                <h2 class="ml-2">Terms</h2>
                <v-row>
                  <v-col cols="12" v-for="prop in paragraph.terms" :key="prop.uri">
                    <v-card>
                      <v-card-text>
                        <v-row align="center" justify="center">
                          <div cols="3" class="headline">{{prop.property}}</div>
                          <v-col cols="7" class="ml-5">
                            <v-select
                              class="predicate"
                              v-model="prop.selected"
                              label="Select a term"
                              :value="prop.selected.uri"
                              :items="prop.result"
                              item-value="uri"
                              :item-text="item => item.prefixedName +' - (score = '+ item.score+' )' +' - (term = '+ item.term+' )'"
                              return-object
                            >
                              <template v-slot:selection="{ item }">
                                <a v-bind:href="item.uri" target="__">{{item.uri}}</a>
                              </template>
                            </v-select>
                          </v-col>
                          <Modal
                            v-if="modalVisible"
                            @close="modalVisible = false"
                            :prop="modalData"
                            :active="modalVisible"
                          ></Modal>
                          <v-btn
                            cols="1"
                            color="blue"
                            dark
                            class="mx-2"
                            fab
                            small
                            @click.stop="modalVisible = true"
                            @click="openModal(prop)"
                          >
                            <v-icon dark>mdi-magnify</v-icon>
                          </v-btn>
                                                  <v-tooltip bottom>
                          <template v-slot:activator="{ on, attrs }">
                            <v-btn
                              color="success"
                              dark
                              class="mx-2"
                              fab
                              v-bind="attrs"
                              v-on="on"
                              small
                              @click.stop="modalCreate = true"
                              @click="openCreateModal(prop)"
                              :table="modalData"
                            >
                              <v-icon dark>mdi-plus</v-icon>
                            </v-btn>
                          </template>
                          <span>Create a class</span>
                        </v-tooltip>

                        </v-row>
                      </v-card-text>
                      <v-divider></v-divider>
                    </v-card>
                  </v-col>
                </v-row>
                <h2 class="ml-2">Entitites</h2>
                <v-col cols="12">
                  <v-data-table :headers="headers" :items="paragraph.entities">
                    <template v-slot:item.uris="{ item }">
                      <v-select label="select a term" v-model="item.selected" :items="item.uris">
                        <template v-slot:selection="{ item }">
                          <a v-bind:href="item" target="__">{{item}}</a>
                        </template>
                      </v-select>
                    </template>
                  </v-data-table>
                </v-col>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </v-tab-item>
    </v-tabs-items>
    <v-tour name="myTour" :steps="steps"></v-tour>
  </v-container>
</template>
<script>
import Modal from "@/Subcomponents/Modal.vue";
import CreateProp from "@/components/modals/CreateProp";
import SearchClass from "@/components/modals/HTML/SearchClass";
import CreateClass from "@/components/modals/HTML/CreateClass";

export default {
  components: {
    Modal,
    CreateProp,
    SearchClass,
    CreateClass
  },
  data() {
    return {
      tab: null,
      modalVisible: false,
      modalData: null,
      modalCreate: false,
      modalSearchClass: false,
      modalCreateClass: false,
      headers: [
        { text: "Entity", value: "text" },
        { text: "URI", value: "uris" }
      ],

      steps: [
        {
          target: "#tables", // We're using document.querySelector() under the hood
          header: {
            title: "Map table elements"
          },
          content: `Map table elements to LOV terms`,
          params: {
            placement: "right"
          }
        },
        {
          target: ".row-class", // We're using document.querySelector() under the hood
          header: {
            title: "Select row class"
          },
          content: `Select a class for table rows`,
          params: {
            enableScrolling: false
          }
        },
        {
          target: ".row-id", // We're using document.querySelector() under the hood
          header: {
            title: "Select row ID"
          },
          content: `Select The ID of each row of the table`,
          params: {
            enableScrolling: false
          }
        },
        {
          target: ".headers", // We're using document.querySelector() under the hood
          header: {
            title: "Map headers"
          },
          content: `Map each header to its LOV term`,
          params: {
            enableScrolling: false
          }
        },

        {
          target: "#paragraphs", // We're using document.querySelector() under the hood
          header: {
            title: "Map paragraphs relations"
          },
          content: `Map paragraphs relations to LOV terms `,
          params: {
            placement: "right"
          }
        },
        {
          target: ".predicate", // We're using document.querySelector() under the hood
          header: {
            title: "Map predicate"
          },
          content: `Map each predicate to LOV terms`,
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
    },
    guide() {
      return this.$store.state.guide;
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
    openModal(data) {
      console.log(data);
      this.modalData = data;
      this.modalVisible = true;
      console.log(this.modalVisible);
    },
    openCreateModal(data) {
      console.log(data);
      this.modalData = data;
      this.modalCreate = true;
    },
    openCreateClassModal(data) {
      console.log(data);
      this.modalData = data;
      this.modalCreateClass = true;
    },

    openSearchClassModal(data) {
      console.log("data=", data);
      this.modalData = data;
      this.modalSearchClass = true;
    },
    updateRowClass(value, table) {
      console.log("value= ", value);
      console.log("table= ", table);
      this.$store.state.csv.rowClass = value;
      this.modalSearchClass = false;
      this.modalCreateClass = false;
    }
  },

  watch: {
    guide(newValue) {
      if (newValue == true) this.$tours["myTour"].start();
      else this.$tours["myTour"].stop();
    },

    count(newCount, oldCount) {
      console.log("old " + oldCount + " new count " + newCount);
      this.results = this.$store.state.properties;
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
    if (this.$store.state.guide) this.$tours["myTour"].start();

    if (this.continue) {
      this.$emit("can-continue", { value: true });
    } else {
      this.$emit("can-continue", { value: false });
    }
  }
};
</script>