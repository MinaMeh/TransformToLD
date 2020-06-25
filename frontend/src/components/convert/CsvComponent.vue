<template>
  <v-container>
    <v-card>
      <v-card-title>Triplets</v-card-title>
      <v-card-text>
        <v-data-table :headers="headers" :items="$store.state.csv.triplets">
          <template v-slot:item.subject="{ item }">
            <a v-bind:href="item.subject">{{item.subject}}</a>
          </template>

          <template v-slot:item.predicate="{ item }">
            <a v-bind:href="item.predicate">{{item.predicate}}</a>
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
      headers: [
        { text: "Subject", value: "subject" },
        { text: "Predicate", value: "predicate" },
        { text: "Object", value: "object" }
      ]
    };
  }
};
</script>