<template>
  <v-container class="px-4 py-0 fill-height" fluid>
    <v-row>
      <v-col cols="12">
        <v-card class="mx-auto text-center" max-width="800">
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
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import CreateProject from "./CreateProject";

export default {
  components: {
    CreateProject
  },
  data() {
    return {
      snackbar: false
    };
  }
};
</script>