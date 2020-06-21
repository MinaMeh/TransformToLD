<template>
  <v-container>
    <Navbar></Navbar>
    <v-card max-width="800" class="mx-auto">
      <v-list-item>
        <v-list-item-content>
          <v-list-item-title class="display-1">Workspace</v-list-item-title>
          <v-list-item-subtitle class="subtitle-1">From Open Data to Linked Data</v-list-item-subtitle>
        </v-list-item-content>
      </v-list-item>
      <v-img src="/logoTitle.png" width="700"></v-img>

      <v-card-text class="title">
        This is the workspace home page. To start linking data choose a project
        or create a new one !
      </v-card-text>

      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="success" class="font-weight-bold">Add project</v-btn>
        <v-btn color="info" class="font-weight-bold">Show projects</v-btn>
      </v-card-actions>
    </v-card>
  </v-container>
</template>
<script>
import Navbar from "@/components/Navbar";
export default {
  components: { Navbar }
};
</script>