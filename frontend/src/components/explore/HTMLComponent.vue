<template>
  <v-container>
    <v-tabs class="mt-8" v-model="tab">
      <v-tab>Tables</v-tab>
      <v-tab>Paragraphs</v-tab>
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
                <v-row>
                  <v-col cols="12" v-for="prop in table.terms" :key="prop.uri">
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
                <v-row>
                  <v-col cols="12" v-for="prop in paragraph.terms" :key="prop.uri">
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
    </v-tabs-items>
  </v-container>
</template>
<script>
import Modal from "@/Subcomponents/Modal.vue";

export default {
  components: {
    Modal
  },  
  data() {
    return {
      tab: null,
      modalVisible: false,
      modalData: null
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
    if (this.continue) {
      this.$emit("can-continue", { value: true });
    } else {
      this.$emit("can-continue", { value: false });
    }
  }
};
</script>