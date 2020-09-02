<template>
  <v-container>
    <v-tabs class="mt-8" v-model="tab">
      <v-tab v-if="vocabularies!=null">Vocabularies</v-tab>
      <v-tab>Relations</v-tab>
      <v-tab>Triplets</v-tab>
    </v-tabs>
    <v-tabs-items v-model="tab">
      <v-tab-item v-if="vocabularies!=null">
        <v-row>
          <v-card>
            <v-card-title>
              <h1 class="headline">Used Vocabularies</h1>
            </v-card-title>
            <v-card-text>
              <v-data-table :headers="vocabsHeaders" :items="vocabularies">
                <template v-slot:item.uri="{ item }">
                  <a v-bind:href="item.uri">{{item.uri}}</a>
                </template>
              </v-data-table>
            </v-card-text>
          </v-card>
        </v-row>
      </v-tab-item>
      <v-tab-item>
        <v-card>
          <v-card-title>
            <h2>Relations</h2>
          </v-card-title>
          <v-card-text>
            <v-data-table :headers="tripletsHeaders" :items="terms"></v-data-table>
          </v-card-text>
        </v-card>
      </v-tab-item>
      <v-tab-item>
        <v-card>
          <v-card-title>
            <h2>Converted Triplets</h2>
          </v-card-title>
          <v-card-text>
            <v-data-table :headers="termsHeaders" :items="triplets">
              <template v-slot:item.subject="{ item }">
                <a v-bind:href="item.subject">{{item.subject}}</a>
              </template>

              <template v-slot:item.predicate="{ item }">
                <a v-bind:href="item.predicate">{{item.predicate}}</a>
              </template>

              <template v-slot:item.object="{ item }">
                <a v-bind:href="item.object" v-if="item.object_type=='url'">{{item.object}}</a>

                <span v-else>{{item.object}}</span>
              </template>
            </v-data-table>
          </v-card-text>
        </v-card>
      </v-tab-item>
    </v-tabs-items>
  </v-container>
</template>

<script>
export default {
  props: {
    vocabularies: Array,
    terms: Array,
    triplets: Array,
  },

  data() {
    return {
      tab: null,
      vocabsHeaders: [
        { text: "Prefix", value: "prefix" },
        { text: "Title", value: "title" },
        { text: "URI", value: "uri" },
      ],
      tripletsHeaders: [
        { text: "Subject", value: "subject" },
        { text: "Predicate", value: "predicate" },
        { text: "Object", value: "object" },
      ],
      termsHeaders: [
        { text: "Subject", value: "subject" },
        { text: "Predicate", value: "predicate" },
        { text: "Object", value: "object" },
      ],
    };
  },
};
</script>