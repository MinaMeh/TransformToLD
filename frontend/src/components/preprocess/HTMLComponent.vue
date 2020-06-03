<template>
  <v-container>
    <v-tabs class="mt-8" v-model="tab">
      <v-tab>Tables</v-tab>
      <v-tab>Paragraphs</v-tab>
    </v-tabs>
    <v-tabs-items v-model="tab">
      <v-tab-item>
        <v-col cols="12">
          <v-card v-for="table in $store.html.tables_selected" :key="table.id" class="mt-3">
            <v-card-title>
              <v-checkbox v-model="tables_selected" :id="table.id" :value="table.id" class="mt-10"></v-checkbox>
              <h2>Table #{{table.id}}</h2>
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
                    <tr v-for="header in table.headers" :key="header.name">
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
        <v-col
          cols="12"
          v-for="(paragraph,index) in $store.csv.paragraphs_selected"
          :key="index"
          class="mt-3"
        >
          <Paragraphs :sentences="paragraph" :id="index"></Paragraphs>
        </v-col>
      </v-tab-item>
    </v-tabs-items>
  </v-container>
</template>
<script>
import Paragraphs from "@/Subcomponents/Paragraphs";

export default {
  name: "HTMLComponent",
  components: {
    Paragraphs
  },
  data() {
    return {
      tab: null,
      continue: true,
      selected: "",
      tables_selected: []
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
    this.$store.state.progress = true;
    if (this.continue) {
      this.$emit("can-continue", { value: true });
    } else {
      this.$emit("can-continue", { value: false });
    }
  }
};
</script>