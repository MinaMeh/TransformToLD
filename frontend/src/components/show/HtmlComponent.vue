<template>
  <v-container>
    <v-tabs class="mt-8" v-model="tab">
      <v-tab>Vocabularies</v-tab>
      <v-tab>Headers</v-tab>
      <v-tab>Relations</v-tab>
      <v-tab>Triplets</v-tab>
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
              <v-data-table :headers="headersHeaders" :items="table.headers">
                <template v-slot:item.selected="{ item }">
                  <v-simple-checkbox v-model="item.selected"></v-simple-checkbox>
                </template>
                <template v-slot:item.term="{ item }">
                  <a v-bind:href="item.term">{{item.term}}</a>
                </template>
                <template v-slot:item.actions="{ item }">
                  <v-btn
                    color="primary"
                    dark
                    class="mx-2"
                    text
                    @click.stop="modalVisible = true"
                    @click="openModal(item)"
                  >
                    <v-icon dark>mdi-pencil-box</v-icon>
                  </v-btn>
                </template>
              </v-data-table>
              <EditTerm
                v-if="modal"
                :modal="modal"
                :term="selectedTerm"
                @edit="edit"
                @close="modal=false"
              ></EditTerm>
            </v-card-text>
          </v-card>
        </v-col>
      </v-tab-item>
      <v-tab-item>
        <v-col cols="12">
          <v-card>
            <v-card-text>
              <v-data-table :headers="termsHeaders" :items="project.terms"></v-data-table>
            </v-card-text>
          </v-card>
        </v-col>
      </v-tab-item>
      <v-tab-item>
        <v-col cols="12">
          <v-card>
            <v-card-text>
              <v-data-table :headers="tripletsHeaders" :items="project.triplets">
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
        </v-col>
      </v-tab-item>
    </v-tabs-items>
  </v-container>
</template>

<script>
import EditTerm from "@/components/modals/EditTerm";

export default {
  components: {
    EditTerm,
  },
  props: {
    project: Object,
  },

  data() {
    return {
      tab: null,
      termsHeaders: [
        { text: "Subject", value: "subject" },
        { text: "Predicate", value: "predicate" },
        { text: "Object", value: "object" },
      ],

      tripletsHeaders: [
        { text: "Subject", value: "subject" },
        { text: "Predicate", value: "predicate" },
        { text: "Object", value: "object" },
      ],

      headersHeaders: [
        { text: "", value: "selected" },
        { text: "Name", value: "name" },
        { text: "Term", value: "term" },
        { text: "Actions", value: "actions" },
      ],

      vocabsHeaders: [
        { text: "Prefix", value: "prefix" },
        { text: "Title", value: "title" },
        { text: "URI", value: "uri" },
      ],
    };
  },
  methods: {
    openModal(data) {
      this.selectedTerm = data;
      this.modal = true;
    },
    edit(value) {
      console.log(value);
      this.modal = false;
      this.$emit("editTerm", value);
    },
  },
};
</script>