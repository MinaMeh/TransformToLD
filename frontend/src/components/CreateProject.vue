<template>
  <v-dialog max-width="900px" v-model="dialog">
    <template v-slot:activator="{ on }">
      <v-btn @click="newProject()" text class="success font-weight-bold" v-on="on">
        <v-icon medium class="mr-1">mdi-file-plus</v-icon>Add new project
      </v-btn>
    </template>
    <v-card>
      <v-card-title class="font-weight-bold text--primary">Add a new project</v-card-title>
      <v-divider></v-divider>
      <v-card-text>
        <v-form class="px-3" ref="form">
          <v-text-field
            outlined
            label="Project Name"
            required
            v-model="project.project_name"
            placeholder="Enter the name of your project"
            prepend-icon="mdi-file"
          ></v-text-field>
          <v-textarea
            outlined
            label="Description"
            v-model="project.description"
            placeholder="Describe your project"
            prepend-icon="mdi-file-document-edit"
          ></v-textarea>
          <v-text-field
            outlined
            label="Licence"
            v-model="project.licence"
            prepend-icon="mdi-file-certificate"
          ></v-text-field>
          <v-text-field
            outlined
            label="Created by"
            v-model="project.author"
            prepend-icon="mdi-account-box"
            readonly
          ></v-text-field>
          <v-row>
            <v-col cols="11" v-if="!link">
              <v-file-input
                outlined
                required
                label="File"
                @change="uploadFile()"
                placeholder="Choose a file"
                v-model="file"
                prepend-icon="mdi-file"
              ></v-file-input>
            </v-col>
            <v-col cols="11" v-if="link">
              <v-text-field
                outlined
                label="File Link"
                placeholder=" File link"
                prepend-icon="mdi-link"
              ></v-text-field>
            </v-col>
            <v-col cols="1">
              <v-switch v-model="link" label="link"></v-switch>
            </v-col>
          </v-row>
          <v-spacer></v-spacer>
          <v-btn text class="font-weight-bold success" @click="saveProject()" :loading="loading">
            <v-icon>mdi-plus</v-icon>Add Project
          </v-btn>
        </v-form>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<script>
import ProjectDataService from "../services/ProjectDataService";

export default {
  name: "add-project",
  data() {
    return {
      project: {
        id: null,
        project_name: "",
        description: "",
        licence: "",
        author: "auteur user name",
        file_link: ""
      },
      link: false,
      file: null,
      type: null,
      loading: false,
      dialog: false
    };
  },

  methods: {
    uploadFile() {
      //console.log(this.file.type);
      //this.$store.state.file_uploaded = this.file;
      this.type = this.file.type;
    },
    saveProject() {
      this.loading = true;
      var data = {
        project_name: this.project.project_name,
        description: this.project.description,
        licence: this.project.licence,
        author: this.project.author,
        file_link: this.project.file_link,
        creation_date: new Date()
      };

      ProjectDataService.create(data)
        .then(response => {
          this.project.id = response.data.id;
          console.log(response.data);

          this.loading = false;
          this.dialog = false;
          this.$emit("projectAdded");
        })
        .catch(e => {
          console.log(e);
        });
    },
    newProject() {
      this.project = {};
    }
  }
};
</script>
