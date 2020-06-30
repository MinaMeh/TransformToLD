<template>
  <v-container>
    <v-tabs class="mt-8" v-model="tab">
      <v-tab>Vocabularies</v-tab>
      <v-tab>Tables</v-tab>
      <v-tab>Paragraphs</v-tab>
    </v-tabs>
    <v-tabs-items v-model="tab">
      <v-tab-item>
        <v-row>
          <v-card>
            <v-card-title>
              <h1 class="headline">Used Vocabularies</h1>
            </v-card-title>
            <v-card-text>
              <v-data-table :headers="vocabsHeaders" :items="project.vocabularies">
                <template v-slot:item.uri="{ item }">
                  <a v-bind:href="item.uri">{{item.uri}}</a>
                </template>
              </v-data-table>
            </v-card-text>
          </v-card>
        </v-row>
      </v-tab-item>
      <v-tab-item>
        <v-col cols="12" v-for="(table,index) in project.html_data.tables" :key="index">
          <v-card>
            <v-card-title>Table #{{index}}</v-card-title>
            <v-card-text>
              <CsvComponent :headers="table.headers" :triplets="table.triplets"></CsvComponent>
            </v-card-text>
          </v-card>
        </v-col>
      </v-tab-item>
      <v-tab-item>
        <v-col cols="12" v-for="(paragraph,index) in project.html_data.paragraphs" :key="index">
          <v-card>
            <v-card-title>Paragraph #{{index}}</v-card-title>
            <v-card-text>
              <TextComponent :triplets="paragraph.triplets" :terms="paragraph.terms"></TextComponent>
            </v-card-text>
          </v-card>
        </v-col>
      </v-tab-item>
    </v-tabs-items>
  </v-container>
</template>

<script>
import { ripple } from "vuetify/lib/directives";
import CsvComponent from "@/components/show/CsvComponent";
import TextComponent from "@/components/show/TextComponent";

export default {
  components: {
    CsvComponent,
    TextComponent
  },
  props: {
    project: Object
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
      ]
    };
  }
};
</script>