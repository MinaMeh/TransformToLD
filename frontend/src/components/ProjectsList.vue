<template>
  <v-container>
    <Navbar></Navbar>
    <v-data-table
      :headers="headers"
      :items="$store.state.projects"
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
      <template v-slot:item="row">
        <tr>
          <td>{{ row.item.id }}</td>
          <td>{{ row.item.project_name }}</td>
          <td>{{ row.item.author.email }}</td>
          <td>{{ row.item.creation_date | formatDate }}</td>
          <td>
            <v-chip small :color="getColor(row.item.status)" dark>
              {{ row.item.status }}
            </v-chip>
          </td>
          <td>
            <v-btn text color="success" medium>
              <a v-bind:href="'/projects/' + row.item.id">
                <v-icon color="info" medium class="mr-2">mdi-eye</v-icon>
              </a>
            </v-btn>
            <v-btn @click="deleteProjectConfirm =true" text>
              <v-icon color="error" medium>mdi-delete</v-icon>
            </v-btn>
          </td>
        </tr>
        <v-dialog v-model="deleteProjectConfirm" width="600">
          <v-card>
            <v-card-title class="headline pt-8" primary-title>
              Confirm Delete
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
                @click="deleteProject(row.item)"
                @projectDeleted="snackbarDelete = true"
                >Delete</v-btn
              >
              <v-btn @click="deleteProjectConfirm = false" dark color="primary"
                >Cancel</v-btn
              >
            </v-card-actions>
            <v-snackbar
              v-model="snackbarDelete"
              :timeout="4000"
              bottom
              color="error"
              ><span>Project Deleted successfully</span>
              <v-btn text color="white" @click="snackbarDelete = false"
                >Close
              </v-btn>
            </v-snackbar>
          </v-card>
        </v-dialog>
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
    deleteProjectConfirm: false,
    snackbarDelete: false,
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
  },
};
</script>
