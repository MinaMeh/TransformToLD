<template>
  <v-container class="mt-10">
    <v-col cols="12">
      <v-card>
        <v-card-text>
          <v-row>
            <v-col cols="5">
              <div class="headline mt-4 mr-2">Table rows are of class</div>
            </v-col>
            <v-col cols="4">
              <v-text-field
                disabled
                v-model="$store.state.csv.rowClass.prefixedName"
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
                    class="mx-2"
                    fab
                    v-bind="attrs"
                    v-on="on"
                    small
                    @click.stop="modalSearchClass = true"
                    @click="openSearchClassModal()"
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
                    @click="openCreateClassModal()"
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
                v-model="$store.state.csv.headersId"
                :items="$store.state.csv.terms"
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
    </v-col>
    <SearchClass
      v-if="modalSearchClass"
      @close="modalSearchClass = false"
      :rowClass="$store.state.csv.rowClass"
      @closeClass="updateRowClass"
      :active="modalSearchClass"
    ></SearchClass>
    <CreateClass
      v-if="modalCreateClass"
      @close="modalCreateClass = false"
      @closeClass="updateRowClass"
      :active="modalCreateClass"
    ></CreateClass>
    <h2>Headers</h2>
    <v-row>
      <v-col cols="12" v-for="prop in $store.state.csv.terms" :key="prop.uri">
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
              <Modal
                v-if="modalVisible"
                @close="modalVisible = false"
                :prop="modalData"
                :active="modalVisible"
              ></Modal>
              <v-tooltip bottom>
                <template v-slot:activator="{ on, attrs }">
                  <v-btn
                    color="blue"
                    dark
                    class="mx-2"
                    fab
                    v-bind="attrs"
                    v-on="on"
                    small
                    @click.stop="modalVisible = true"
                    @click="openModal(prop)"
                  >
                    <v-icon dark>mdi-magnify</v-icon>
                  </v-btn>
                </template>
                <span>Search another property</span>
              </v-tooltip>

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
            </v-row>
          </v-card-text>
          <v-divider></v-divider>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import Modal from "@/Subcomponents/Modal.vue";
import CreateProp from "@/components/modals/CreateProp";
import SearchClass from "@/components/modals/SearchClass";
import CreateClass from "@/components/modals/CreateClass";

export default {
  name: "CsvComponent",
  components: {
    Modal,
    CreateProp,
    SearchClass,
    CreateClass
  },
  props: {
    terms: Array
  },
  data() {
    return {
      continue: true,
      search: "",
      selected: "",
      addDialog: false,
      searchDialog: false,
      modalVisible: false,
      modalData: null,
      modalCreate: false,
      modalSearchClass: false,
      modalCreateClass: false
    };
  },
  computed: {},
  methods: {
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
      this.modalCreateClass = true;
    },

    openSearchClassModal(data) {
      console.log(data);
      this.modalSearchClass = true;
    },
    updateRowClass(value) {
      console.log("value= ", value);
      this.$store.state.csv.rowClass = value;
      this.modalSearchClass = false;
      this.modalCreateClass = false;
    }
  },
  watch: {
    count(newCount, oldCount) {
      console.log("old " + oldCount + " new count " + newCount);
      this.properties = this.$store.state.properties;
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
    if (this.continue) {
      this.$emit("can-continue", { value: true });
    } else {
      this.$emit("can-continue", { value: false });
    }
  }
};
</script>
