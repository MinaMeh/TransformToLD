<template>
  <v-container>
    <v-tabs class="mt-8" v-model="tab">
      <v-tab>Tables</v-tab>
      <v-tab>Paragraphs</v-tab>
    </v-tabs>
    <v-tabs-items v-model="tab">
      <v-tab-item>
        <v-row>
          <v-col cols="12" v-for="table in $store.state.html.tables_triplets " :key="table.id">
            <v-card>
              <v-card-title>Triplets of table {{table.id}}</v-card-title>
              <v-card-text>
                <v-data-table :headers="headers" :items="table.triplets">
                  <template v-slot:item.subject="{ item }">
                    <a v-bind:href="item.subject">{{item.subject}}</a>
                  </template>

                  <template v-slot:item.predicate="{ item }">
                    <a v-bind:href="item.predicate">{{item.predicate}}</a>
                  </template>
                </v-data-table>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </v-tab-item>
      <v-tab-item>
        <v-row>
          <v-col
            cols="12"
            v-for="paragraph in $store.state.html.paragraphs_triplets"
            :key="paragraph.id"
          >
            <v-card>
              <v-card-title>Triplets of paragraph {{paragraph.id}}</v-card-title>
              <v-card-text>
                <v-data-table :headers="headers" :items="paragraph.triplets">
                  <template v-slot:item.subject="{ item }">
                    <a v-bind:href="item.subject">{{item.subject}}</a>
                  </template>

                  <template v-slot:item.predicate="{ item }">
                    <a v-bind:href="item.predicate">{{item.predicate}}</a>
                  </template>
                </v-data-table>
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
      tab: null,

      headers: [
        { text: "Subject", value: "subject" },
        { text: "Predicate", value: "predicate" },
        { text: "Object", value: "object" }
      ]
    };
  }
};
</script>