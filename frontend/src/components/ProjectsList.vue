<template>
  <v-container>
    <Navbar></Navbar>
    <v-data-table
      :headers="headers"
      :items="$store.state.projects"
      sort-by="id"
      class="elevation-1"
      :search="search"
    >
      <template v-slot:top>
        <v-toolbar flat color="white">
          <v-toolbar-title>Projects List</v-toolbar-title>
          <v-divider class="mx-4" inset vertical></v-divider>
          <v-spacer></v-spacer>
          <v-text-field
            v-model="search"
            append-icon="mdi-magnify"
            label="Search"
            single-line
            hide-details
          ></v-text-field>
          <v-spacer></v-spacer>
        </v-toolbar>
      </template>
      <template v-slot:item.status="{ item }">
        <v-chip small :color="getColor(item.status)" dark>{{
          item.status
        }}</v-chip>
      </template>
      <template v-slot:item.author="{ item }">
        <p>{{ item.author.email }}</p>
      </template>
      <template v-slot:item.creation="{ item }">
        <p>{{ item.creation_date | formatDate }}</p>
      </template>
      <template v-slot:item.actions="{ item }">
        <v-btn text color="success" medium>
          <a v-bind:href="'/projects/' + item.id">
            <v-icon color="info" medium class="mr-2">mdi-eye</v-icon>
          </a>
        </v-btn>
        <v-icon color="error" medium @click="deleteProjectConfirm = true"
          >mdi-delete</v-icon
        >
        <v-dialog v-model="deleteProjectConfirm" width="600">
          <v-card>
            <v-card-title class="headline pt-8" primary-title
              >Confirm Delete</v-card-title
            >
            <v-divider></v-divider>
            <v-card-text class="pl-8 font-weight-bold"
              >are you sure ? You want to delete this project ?</v-card-text
            >
            <v-card-actions class="pa-5">
              <v-btn
                dark
                class="ml-auto"
                color="error"
                @click="deleteProject(item)"
                @projectDeleted="snackbarDelete = true"
                >Delete</v-btn
              >
              <v-btn @click="deleteProjectConfirm = false" dark color="primary"
                >Cancel</v-btn
              >
            </v-card-actions>
          </v-card>
        </v-dialog>
        <v-snackbar
          v-model="snackbarDelete"
          :timeout="4000"
          bottom
          color="error"
        >
          <span>Project Deleted successfully</span>
          <v-btn text color="white" @click="snackbarDelete = false"
            >Close</v-btn
          >
        </v-snackbar>
      </template>
      <template v-slot:no-data>
        <v-card class="mx-auto" max-width="500">
          <v-card-text>
            <p class="text-center font-weight-bold red--text">
              There is no project !
            </p>
          </v-card-text>
        </v-card>
      </template>
    </v-data-table>
  </v-container>
</template>

<script>
import Navbar from "@/components/Navbar";
import axios from "axios";
export default {
  components: {
    Navbar,
  },
  data: () => ({
    dialog: false,
    search: "",
    loading: true,
    headers: [
      { text: "Id", value: "id", align: "start", sortable: true },
      { text: "Project Name", value: "project_name" },
      { text: "Project author", value: "author" },
      { text: "Creation date", value: "creation" },
      { text: "Conversion Status", value: "status" },
      { text: "Actions", value: "actions", sortable: false },
    ],
    snackbarDelete: false,
    deleteProjectConfirm: false,
  }),

  mounted() {
    this.getAllProjects();
  },

  methods: {
    getAllProjects() {
      axios
        .get("http://127.0.0.1:8000/api/projects")
        .then((response) => {
          this.$store.state.projects = response.data;
          console.log(this.$store.state.projects.length);
          console.log(response.data);
          this.loading = false;
        })
        .catch((error) => console.log(error));
    },
    getColor(status) {
      if (status == "converted") return "green";
      else return "red";
    },

    deleteProject(item) {
      const index = this.$store.state.projects.indexOf(item);
      console.log("index = " + index);
      axios
        .delete(`http://127.0.0.1:8000/api/projects/` + item.id)
        .then((response) => {
          console.log("id = " + item.id);
          console.log(response.data);
          console.log(this.$store.state.projects.length);
          this.deleteProjectConfirm = false;
          this.snackbarDelete = true;
          this.$store.state.projects.splice(index, 1);
          this.get;
        })
        .catch((error) => console.log(error));
    },
  },
};
</script>
