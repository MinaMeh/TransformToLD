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
                dense
                :headers="headers"
                :items="projects"
                sort-by="id"
                class="elevation-1"
                :search="search"
                @click:row="goToproject"
              >
                <template v-slot:item.converted="{ item }">
                  <v-chip
                    class="mt-2"
                    v-if="(item.converted == false)"
                    small
                    color="red"
                    dark
                  >Not converted</v-chip>
                  <v-chip
                    class="mt-2"
                    v-if="(item.converted == true)"
                    small
                    color="green"
                    dark
                  >Converted</v-chip>
                </template>
                <template v-slot:item.input="{ item }">
                  <v-chip class="mt-2" small color="primary">{{item.input_file.file_type}}</v-chip>
                </template>

                <template v-slot:item.creation="{ item }">
                  <p>{{ item.creation_date | formatDate }}</p>
                </template>
                <template v-slot:item.actions="{ item }">
                  <ConfirmDeletion
                    v-if="modalVisible"
                    @close="close()"
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
import ConfirmDeletion from "@/components/projects/DeleteProjectComponent";
import instance from "@/services/MainService";
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
      { text: "Input File Type", value: "input" },
      { text: "Creation date", value: "creation" },
      { text: "Status", value: "converted" },
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
    close() {
      this.modalVisible = false;
      this.getAllProjects();
    },
    getAllProjects() {
      console.log(this.$store.state.user.email);
      instance
        .get("/api/projects", {
          headers: {
            "Content-Type": "multipart/form-data",
            Authorization: `JWT ${this.$store.state.jwt}`
          },
          params: {
            user_id: this.$store.state.user_id
          }
        })
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
    },
    goToproject(value) {
      console.log("id", value.id);
      this.$router.push("/projects/" + value.id);
    }
  }
};
</script>
