<template>
  <v-dialog v-model="active" width="600">
    <v-card>
      <v-card-title class="headline pt-8" primary-title>
        Confirm Deletion of {{ project.project_name }}
      </v-card-title>
      <v-divider></v-divider>
      <v-card-text class="pl-8 font-weight-bold">
        are you sure ? You want to delete this project ?
      </v-card-text>
      <v-card-actions class="pa-5">
        <v-btn
          dark
          class="ml-auto"
          color="error"
          @click="deleteProject(item)"
          @projectDeleted="snackbarDelete = true"
        >
          Delete</v-btn
        >
        <v-btn @click="deleteProjectConfirm = false" dark color="primary">
          Cancel
        </v-btn>
      </v-card-actions>
      <v-snackbar v-model="snackbarDelete" :timeout="4000" bottom color="error"
        ><span>Project Deleted successfully</span>
        <v-btn text color="white" @click="snackbarDelete = false">
          Close
        </v-btn>
      </v-snackbar>
    </v-card>
  </v-dialog>
</template>

<script>
import axios from "axios";
export default {
  props: ["project", "active"],

  data(){
      return{
        snackbarDelete : false,
      }

  },
  methods: {
       deleteProject(item) {
      axios
        .delete(`http://127.0.0.1:8000/api/projects/` + item.id)
        .then((response) => {
          console.log("id = " + item.id);
          console.log(response.data);
          console.log(this.$store.state.projects.length);
          this.deleteProjectConfirm = false;
          this.snackbarDelete = true;
          this.getAllProjects();
        })
        .catch((error) => console.log(error));
    },
  },
};
</script>
