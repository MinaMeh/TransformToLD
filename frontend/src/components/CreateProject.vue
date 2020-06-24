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
        <v-form class="px-3">
          <v-text-field
            outlined
            label="Project Name"
            required
            v-model="$store.state.project_name"
            placeholder="Enter the name of your project"
            prepend-icon="mdi-file"
          ></v-text-field>
          <v-textarea
            outlined
            label="Description"
            v-model="$store.state.description"
            placeholder="Describe your project"
            prepend-icon="mdi-file-document-edit"
          ></v-textarea>
          <v-text-field
            outlined
            label="Licence"
            v-model="$store.state.licence"
            prepend-icon="mdi-file-certificate"
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
          <v-row v-if="type != null">
            <v-col cols="6">
              <v-text-field
                disabled
                outlined
                label="File format"
                v-model="type"
                prepend-icon="mdi-file-document"
              ></v-text-field>
            </v-col>
            <v-col cols="6" v-if="type == 'text/csv' || type =='application/vnd.ms-excel'">
              <v-text-field
                outlined
                label="Separator"
                placeholder=" example: ; , | ! "
                v-model="$store.state.csv.separator"
                prepend-icon="mdi-file-delimited"
              ></v-text-field>
            </v-col>
            <v-col cols="6" v-if="type == 'text/html'">
              <v-row justify="space-around">
                <v-checkbox
                  outlined
                  label="Extract tables"
                  v-model="$store.state.html.extract_tables"
                ></v-checkbox>
                <v-checkbox
                  outlined
                  label="Extract paragraphs"
                  v-model="$store.state.html.extract_paragraphs"
                ></v-checkbox>
              </v-row>
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
import axios from "axios";
import { validationMixin } from "vuelidate";

export default {
  mixins: [validationMixin],
  name: "add-project",
  data() {
    return {
      form: {
        project_name: "",
        description: "",
        licence: "",
        file_link: ""
      },
      html: {
        tables: true,
        paragraphs: true
      },
      link: false,
      file: null,
      type: null,
      filename: "No file uploaded",
      csv: {
        separator: ";"
      },
      loading: false,
      dialog: false
    };
  },
  methods: {
    uploadFile() {
      console.log(this.file.type);
      this.$store.state.file_uploaded = this.file;
      this.type = this.file.type;
    },
    saveProject() {
      this.loading = true;
      var formData = new FormData();
      var project = {
        project_name: this.$store.state.project_name,
        description: this.$store.state.description,
        licence: this.$store.state.licence,
        author: this.$store.state.user,
        creation_date: new Date()
      };
      formData.append("project", JSON.stringify(project));
      formData.append("file", this.$store.state.file_uploaded);
      formData.append("project_name", this.$store.state.project_name);
      formData.append("description", this.$store.state.description);
      formData.append("licence", this.$store.state.licence);
      formData.append("separator", this.$store.state.csv.separator);
      formData.append("tables", this.$store.state.html.extract_tables);
      formData.append("paragraphs", this.$store.state.html.extract_paragraphs);
      axios
        .post("http://localhost:8000/extract/", formData, {
          headers: {
            "Content-Type": "multipart/form-data"
          }
        })
        .then(response => {
          console.log(response.data);
          this.$store.state.filename = response.data.filename;
          this.$store.state.file_type = response.data.type;
          this.$store.state.size = response.data.size;

          if (response.data.type == "csv") {
            this.$store.state.csv.headers = response.data.results.headers;
            this.$store.state.csv.columns = response.data.results.columns;
            this.$store.state.csv.lines = response.data.results.lines;
          }
          if (response.data.type == "html") {
            this.$store.state.html.tables = response.data.results.tables;
            this.$store.state.html.paragraphs =
              response.data.results.paragraphs;
            this.$store.state.html.num_paragraphs =
              response.data.results.num_paragraphs;
            this.$store.state.html.num_tables =
              response.data.results.num_tables;
          }
          if (response.data.type == "text") {
            this.$store.state.text.paragraph = response.data.results.paragraph;
            this.$store.state.text.sentences = response.data.results.sentences;
          }

          this.$store.state.progress = false;

          this.loading = false;
          this.dialog = false;
          this.$emit("projectAdded");
        })
        .catch(error => console.log(error));
    },

    newProject() {
      this.project = {};
    }
  }
};
</script>
