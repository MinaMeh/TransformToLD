<template>
  <v-container>
    <Navbar></Navbar>
    <v-card max-width="800" class="mx-auto">
      <v-list-item>
        <v-list-item-content>
          <v-list-item-title class="display-1">Workspace</v-list-item-title>
          <v-list-item-subtitle class="subtitle-1"
            >From Open Data to Linked Data</v-list-item-subtitle
          >
        </v-list-item-content>
      </v-list-item>
      <v-img src="/logoTitle.png" width="700"></v-img>
      <v-card-text class="title">
        This is the workspace home page. To start linking data choose a project
        or create a new one !
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <CreateProject @projectAdded="snackbar = true"></CreateProject>
        <v-btn color="primary" class="font-weight-bold" to="/projects-list">
          <v-icon medium class="mr-1">mdi-file-eye</v-icon>Show projects
        </v-btn>
      </v-card-actions>
      <v-snackbar v-model="snackbar" :timeout="4000" top color="success">
        <span>Awesome! You added a new project.</span>
        <v-btn text color="white" @click="snackbar = false">Close</v-btn>
      </v-snackbar>
    </v-card>
  </v-container>
</template>
<script>
import Navbar from "@/components/Navbar";
import CreateProject from "./CreateProject";
export default {
  data() {
    return {
      snackbar: false,
    };
  },
  components: { Navbar, CreateProject },
};
</script>
