<template>
  <v-container>
    <Navbar></Navbar>
    <v-data-table
      :headers="headers"
      :items="$store.state.projects"
      :search="search"
    >
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
            <confirmModel
              text
              color="error"
              v-if="modalVisible"
              @close="modalVisible = false"
              :item="modalData"
              :active="modalVisible"
              message="Are you sure you want to delete this project?"
            >
            </confirmModel>
            <v-btn text @click.stop="modalVisible = true" @click="openModal(item)">
              <v-icon text color="error" medium class="mr-2">mdi-delete</v-icon>
            </v-btn>
            
          </td>
        </tr>
      </template>
    </v-data-table>
  </v-container>
</template>

<script>
import Navbar from "@/components/Navbar";
import confirmModel from "@/components/confirm";
import axios from "axios";
export default {
  components: {
    Navbar,
    confirmModel,
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

    modalVisible: false,
    modalData: null,
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

    openModal(data) {
      console.log(data);
      this.modalData = data;
      this.modalVisible = true;
      console.log(this.modalVisible);
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
