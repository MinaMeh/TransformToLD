<template>
  <v-container>
    <v-tabs class="mt-8" v-model="tab">
      <v-tab v-if="vocabularies!=null">Vocabularies</v-tab>
      <v-tab>Headers</v-tab>
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
            <h2>Headers</h2>
          </v-card-title>
          <v-card-text>
            <v-data-table :headers="headersHeaders" :items="headers">
              <template v-slot:item.selected="{ item }">
                <v-simple-checkbox v-model="item.selected"></v-simple-checkbox>
              </template>
              <template v-slot:item.term="{ item }">
                <a v-bind:href="item.term">{{item.term}}</a>
              </template>
            </v-data-table>
          </v-card-text>
        </v-card>
      </v-tab-item>
      <v-tab-item>
        <v-card>
          <v-card-title>
            <h2>Triplets</h2>
          </v-card-title>
          <v-card-text>
            <v-data-table :headers="tripletsHeaders" :items="triplets">
              <template v-slot:item.subject="{ item }">
                <a v-bind:href="item.subject">{{item.subject}}</a>
              </template>

              <template v-slot:item.predicate="{ item }">
                <a v-bind:href="item.predicate">{{item.predicate}}</a>
              </template>
            </v-data-table>
          </v-card-text>
        </v-card>
      </v-tab-item>
    </v-tabs-items>
  </v-container>
</template>

<script>
import { ripple } from "vuetify/lib/directives";

export default {
  props: {
    vocabularies: Array,
    triplets: Array,
    headers: Array
  },
  directives: {
    ripple
  },

  data() {
    return {
      tab: null,
      vocabsHeaders: [
        { text: "Prefix", value: "prefix" },
        { text: "Title", value: "title" },
        { text: "URI", value: "uri" }
      ],
      headersHeaders: [
        { text: "", value: "selected" },
        { text: "Name", value: "name" },
        { text: "Term", value: "term" }
      ],
      tripletsHeaders: [
        { text: "Subject", value: "subject" },
        { text: "Predicate", value: "predicate" },
        { text: "Object", value: "object" }
      ]
    };
  }
};
</script>