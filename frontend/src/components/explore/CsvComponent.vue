<template>
  <v-container class="mt-10">
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
              <!-- <v-dialog v-model="addDialog" width="800">
                <template v-slot:activator="{ on, attrs }">
                  <v-btn color="green" dark v-bind="attrs" v-on="on" class="mx-2" fab small>
                    <v-icon dark>mdi-plus</v-icon>
                  </v-btn>
                </template>
                <v-card>
                  <v-card-title>Add new property</v-card-title>
                  <v-card-text>
                    <v-container>
                      <v-row>
                        <v-col cols="12">
                          <v-text-field label="Domain Name"></v-text-field>
                        </v-col>
                        <v-col cols="12">
                          <v-text-field label="Property Name"></v-text-field>
                        </v-col>
                        <v-col cols="12">
                          <v-textarea
                            label="Property Description"
                            hint="Add description to show what this property means and some examples about its uses"
                          ></v-textarea>
                        </v-col>
                      </v-row>
                    </v-container>
                  </v-card-text>
                  <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn color="red darken-1" text @click="addDialog = false">Close</v-btn>
                    <v-btn color="green darken-1" text @click="addDialog = false">Save</v-btn>
                  </v-card-actions>
                </v-card>
              </v-dialog>-->
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
  </v-container>
</template>

<script>
import Modal from "@/Subcomponents/Modal.vue";
export default {
  name: "CsvComponent",
  components: {
    Modal
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
      modalData: null
    };
  },
  computed: {},
  methods: {
    openModal(data) {
      console.log(data);
      this.modalData = data;
      this.modalVisible = true;
      console.log(this.modalVisible);
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
