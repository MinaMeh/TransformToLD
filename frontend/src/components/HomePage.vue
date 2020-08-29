<template>
  <v-container>
    <v-card max-width="800" class="mx-auto">
      <v-list-item>
        <v-list-item-content>
          <v-list-item-title class="display-1">Workspace</v-list-item-title>
          <v-list-item-subtitle class="subtitle-1">From Open Data to Linked Data</v-list-item-subtitle>
        </v-list-item-content>
      </v-list-item>
      <v-img src="/logoTitle.png" width="700"></v-img>
      <v-card-text class="title">
        DataLinked is a plateform to transform you dataset to linked data
        <br />The tool converts csv, text, html, pdf and image files into linked data represented as an RDF Graph.
        <br />You can download the transformed dataset as turtle, XML, JSON, N3, NT, NQUADS, Trix or Trig files.
        <br />If you want to control conversion parameters login as an expert user.
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="success" class="font-weight-bold" to="/projects-list">
          <v-icon medium class="mr-1">mdi-account-star</v-icon>Login As Expert
        </v-btn>
        <v-btn color="primary" class="font-weight-bold" to="/projects-list">
          <v-icon medium class="mr-1">mdi-swap-horizontal</v-icon>Convert Dataset
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-container>
</template>
<script>
export default {};
</script>