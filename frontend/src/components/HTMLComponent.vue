<template>
  <v-container>
    <v-tabs class="mt-8" v-model="tab">
      <v-tab>Tables</v-tab>
      <v-tab>Paragraphs</v-tab>
    </v-tabs>
    <v-tabs-items v-model="tab">
      <v-tab-item>
        <v-row>
          <v-col cols="12" v-for="table in results.results.tables" :key="table.id">
            <v-card>
              <v-card-title>
                <h2 class="mt-3">Table #{{table.id +1}}</h2>
              </v-card-title>
              <v-card-text>
                <v-row>
                  <v-col cols="6" v-for="prop in table.terms" :key="prop.uri">
                    <v-card color="grey lighten-4">
                      <v-card-text>
                        <v-row no-gutters align="center" justify="center">
                          <vcol cols="4" class="mt-5">
                            <h4>{{prop.property}}</h4>
                          </vcol>
                          <v-col cols="8" class="ml-5">
                            <v-select
                              class="mt-8"
                              dense
                              outlined
                              label="Select a term"
                              :items="prop.result"
                              item-value="uri"
                              :item-text="item => item.prefixedName +' - (score = '+ item.score+' )'"
                              return-object
                            ></v-select>
                          </v-col>
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
          <v-col cols="12" v-for="(paragraph,index) in results.results.paragraphs" :key="index">
            <v-card>
              <v-card-title>
                <h2>Paragraph #{{index+1}}</h2>
              </v-card-title>
              <v-card-text>
                <v-row>
                  <v-col cols="12" class="mb-5">{{paragraph.paragraph}}</v-col>
                  <v-col cols="12">
                    <v-card>
                      <v-card-text>
                        <h4 class="text-center">Entities</h4>
                        <v-simple-table dense class="ml-5">
                          <thead>
                            <tr>
                              <th>Entity</th>
                              <th>Class</th>
                              <th>URI</th>
                            </tr>
                          </thead>
                          <tbody>
                            <tr
                              v-for="(entity, index) in paragraph.entities"
                              @click="show(entity)"
                              :key="index"
                            >
                              <td>{{entity.name}}</td>

                              <td class="caption ml-3">
                                <v-select
                                  dense
                                  outlined
                                  menu-props="auto"
                                  :items="entity.entity_type"
                                  v-model="entity.entity_type[0].prefixedName"
                                  item-value="prefixedName"
                                  item-text="prefixedName"
                                ></v-select>
                              </td>
                              <td class="caption ml-3">
                                <v-select
                                  dense
                                  outlined
                                  menu-props="auto"
                                  :items="entity.uri"
                                  v-model="entity.uri[0]"
                                  item-value="uri"
                                  item-text="uri"
                                ></v-select>
                              </td>
                            </tr>
                          </tbody>
                        </v-simple-table>
                      </v-card-text>
                    </v-card>
                  </v-col>
                  <v-col cols="12">
                    <v-card>
                      <v-card-text>
                        <h4 class="text-center" self-align="center">RDF Triples</h4>
                        <v-simple-table class="ml-5" dense>
                          <thead>
                            <tr>
                              <th>Subject</th>
                              <th>Predicate</th>
                              <th>Object</th>
                            </tr>
                          </thead>
                          <tbody>
                            <tr v-for="(triple,index) in triples" :key="index">
                              <td>{{triple.subject}}</td>
                              <td>{{triple.predicat}}</td>
                              <td>{{triple.object}}</td>
                            </tr>
                          </tbody>
                        </v-simple-table>
                      </v-card-text>
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
export default {
  data() {
    return {
      results: null,
      tab: null,
      triples: [{ subject: "test", predicat: "test", object: "test" }]
    };
  },
  methods: {
    show(payload) {
      console.log(payload);
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
  computed: {
    count() {
      return this.$store.state.properties.length;
    }
  },
  mounted() {
    this.results = this.$store.state.properties;
    if (this.continue) {
      this.$emit("can-continue", { value: true });
    } else {
      this.$emit("can-continue", { value: false });
    }
  }
};
</script>