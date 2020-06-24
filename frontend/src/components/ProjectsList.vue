<template>
  <v-container>
    <Navbar></Navbar>
    <v-data-table
      :headers="headers"
      :items="projects"
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
      <template v-slot:item.actions="{ }">
        <v-btn text color="success" medium to="/projects/:id">
          <v-icon medium class="mr-2">mdi-eye</v-icon>
        </v-btn>
        <v-btn text medium to="/transform">
          <v-icon medium class="mr-2">mdi-file-sync</v-icon>
        </v-btn>
      </template>
      <template v-slot:no-data>
        <v-card class="mx-auto" max-width="500">
          <v-card-text>
            <p class="text-center font-weight-bold red--text">There is no project !</p>
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
    Navbar
  },
  data: () => ({
    dialog: false,
    search: "",
    loading: true,
    projects: [],
    headers: [
      { text: "Id", value: "id", align: "start", sortable: true },
      { text: "Project Name", value: "project_name" },
      { text: "Project author", value: "author" },
      { text: "Creation date", value: "creation_date" },
      { text: "Conversion Status", value: "converted" },
      { text: "Actions", value: "actions", sortable: false }
    ],

    currentProject: null,
    currentIndex: -1
  }),

  mounted() {
    this.getAllProjects();
  },

  methods: {
    getAllProjects() {
      axios
        .get("http://127.0.0.1:8000/api/projects")
        .then(response => {
          this.projects = response.data;
          console.log(this.projects.length);
          this.loading = false;
        })
        .catch(error => console.log(error));
    },

    setActiveProject(project, index) {
      (this.currentProject = project), (this.currentIndex = index);
    }
  }
};
</script>
