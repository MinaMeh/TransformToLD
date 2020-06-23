<template>
  <v-container>
    <v-data-table
      :headers="headers"
      :items="projects"
      sort-by="name"
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
          <v-dialog v-model="dialog" max-width="500px">
            <template v-slot:activator="{ on }">
              <v-btn color="success" dark small class="mb-2 font-weight-bold" v-on="on">New Project</v-btn>
            </template>
            <v-card>
              <v-card-title>
                <span class="headline">{{ formTitle }}</span>
              </v-card-title>

              <v-card-text>
                <v-container>
                  <v-row>
                    <v-text-field v-model="editedItem.name" label="Project name" required></v-text-field>
                  </v-row>
                  <v-row>
                    <v-textarea v-model="editedItem.description" label="Description" required></v-textarea>
                  </v-row>
                  <v-row>
                    <v-select
                      v-model="editedItem.licence"
                      :items="licences"
                      label="Licence"
                      required
                    ></v-select>
                  </v-row>
                </v-container>
              </v-card-text>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn small dark color="error" @click="close">Cancel</v-btn>
                <v-btn small dark color="secondary" @click="save">Save</v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>
        </v-toolbar>
      </template>
      <template v-slot:item.actions="{ item }">
        <v-btn text color="success" medium to="/Project">
          <v-icon medium class="mr-2">mdi-eye</v-icon>
        </v-btn>
        <v-icon color="primary" medium class="mr-2" @click="editItem(item)">mdi-pencil</v-icon>
        <v-icon color="error" medium @click="deleteItem(item)">mdi-delete</v-icon>
      </template>
      <template v-slot:no-data>
        <v-btn color="primary" @click="initialize">Reset</v-btn>
      </template>
    </v-data-table>
  </v-container>
</template>

<script>
export default {
  data: () => ({
    dialog: false,
    search: "",
    headers: [
      {
        text: "Project Name",
        align: "start",
        sortable: true,
        value: "name"
      },
      { text: "Project's Author", value: "Author" },
      { text: "Creation date", value: "CreationDate" },
      { text: "Actions", value: "actions", sortable: false }
    ],
    projects: [],
    licences: [],
    editedIndex: -1,
    editedItem: {
      name: "",
      description: "",
      licence: "",
      Author: "",
      CreationDate: ""
    },
    defaultItem: {
      name: "",
      description: "",
      licence: "",
      Author: "",
      CreationDate: ""
    }
  }),

  computed: {
    formTitle() {
      return this.editedIndex === -1 ? "New Project" : "Edit Project";
    }
  },

  watch: {
    dialog(val) {
      val || this.close();
    }
  },

  created() {
    this.initialize();
  },

  methods: {
    initialize() {
      this.projects = [
        {
          name: "KitKat",
          description: "informations",
          licence: "Item 1",
          Author: "imene gmail",
          CreationDate: "Date 1"
        },
        {
          name: "Eclair",
          description: "infos",
          licence: "Item 2",
          Author: "amina",
          CreationDate: "Date 2"
        }
      ];
      this.licences = ["Item 1", "Item 2", "Item 3", "Item 4"];
    },

    editItem(item) {
      this.editedIndex = this.projects.indexOf(item);
      this.editedItem = Object.assign({}, item);
      this.dialog = true;
    },

    showItem(item) {
      const index = this.projects.indexOf(item);
      this.projects.value(index);
    },

    deleteItem(item) {
      const index = this.projects.indexOf(item);
      confirm("Are you sure you want to delete this item?") &&
        this.projects.splice(index, 1);
    },

    close() {
      this.dialog = false;
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem);
        this.editedIndex = -1;
      });
    },

    save() {
      if (this.editedIndex > -1) {
        Object.assign(this.projects[this.editedIndex], this.editedItem);
      } else {
        this.projects.push(this.editedItem);
      }
      this.close();
    }
  }
};
</script>
