<template>
  <v-container>
    <v-card>
      <v-card-title>Triplets</v-card-title>
      <v-card-text>
        <v-data-table :headers="headers" :items="$store.state.text.triplets" show-expand>
          <template v-slot:item.subject="{ item }">
            <a v-bind:href="item.subject">{{item.subject}}</a>
          </template>

          <template v-slot:item.predicate="{ item }">
            <a v-bind:href="item.predicate">{{item.predicate}}</a>
          </template>
          <template v-slot:item.object="{ item }">
            <a v-bind:href="item.predicate" v-if="item.object_type=='url'">{{item.object}}</a>
            <span v-else>{{item.object}}</span>
          </template>
        </v-data-table>
      </v-card-text>
    </v-card>
  </v-container>
</template>
<script>
export default {
  data() {
    return {
      expanded: [],

      headers: [
        { text: "Subject", value: "subject" },
        { text: "Predicate", value: "predicate" },
        { text: "Object", value: "object" }
      ]
    };
  }
};
</script>