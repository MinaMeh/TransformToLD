<template>
  <v-container>
    <Navbar></Navbar>
    <v-row>
      <v-col cols="12">
        <v-card>
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
          <v-card-text>
            <v-col cols="12">
              <v-data-table
                :headers="headers"
                :items="projects"
                sort-by="id"
                class="elevation-1"
                :search="search"
              >
                <template v-slot:item.status="{ item }">
                  <v-chip v-if="item.status=false" small color="green" dark>{{ item.converted }}</v-chip>
                  <v-chip v-if="item.status=true" small color="red" dark>{{ item.converted }}</v-chip>              
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
                  <ConfirmDeletion
                    v-if="modalVisible"
                    @close="modalVisible = false"
                    :item="modalData"
                    :confirmDelete="modalVisible"
                  ></ConfirmDeletion>
                  <v-btn
                    color="error"
                    dark
                    class="mx-2"
                    text
                    medium
                    @click.stop="modalVisible = true"
                    @click="openModal(item)"
                  >
                    <v-icon dark>mdi-delete</v-icon>
                  </v-btn>
                </template>
                <template v-slot:no-data>
                  <v-card class="mx-auto" max-width="500">
                    <v-card-text>
                      <p
                        class="text-center font-weight-bold red--text mt-5"
                      >There is no project yet!</p>
                    </v-card-text>
                  </v-card>
                </template>
              </v-data-table>
            </v-col>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import Navbar from "@/components/Navbar";
import ConfirmDeletion from "@/components/DeleteProjectComponent";
import axios from "axios";
export default {
  components: {
    Navbar,
    ConfirmDeletion
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
      { text: "Actions", value: "actions", sortable: false }
    ],
    snackbarDelete: false,
    deleteProjectConfirm: false,
    modalVisible: false,
    modalData: null,
    projects: []
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
          console.log(response.data);
          this.loading = false;
        })
        .catch(error => console.log(error));
    },

    openModal(data) {
      console.log(data);
      this.modalData = data;
      this.modalVisible = true;
      console.log(this.modalVisible);
    }
  }
};
</script>
