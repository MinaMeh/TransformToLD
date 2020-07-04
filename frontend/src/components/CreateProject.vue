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
            :rules="nameRules"
            :counter="10"
            required
            v-model="$store.state.project_name"
            placeholder="Enter the name of your project"
            prepend-icon="mdi-file"
          ></v-text-field>
          <v-row>
            <v-col cols="11" v-if="!link">
              <v-file-input
                show-size
                accept="image/png, image/jpeg, text/html, text/plain, text/csv, application/pdf, application/vnd.ms-excel, application/msword, application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                outlined
                required
                label="File"
                :rules="fileRules"
                @change="uploadFile()"
                placeholder="Choose a file"
                v-model="file"
                prepend-icon="mdi-file-link"
              ></v-file-input>
            </v-col>
            <v-col cols="11" v-if="link">
              <v-text-field
                outlined
                :rules="linkRules"
                required
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
            <v-col cols="6" v-if="type == 'text/csv' || type == 'application/vnd.ms-excel'">
              <v-text-field
                outlined
                label="Separator"
                placeholder=" example: ; , | ! "
                v-model="$store.state.csv.separator"
                prepend-icon="mdi-file-table"
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
            <v-icon>mdi-plus</v-icon>Create
          </v-btn>
        </v-form>
      </v-card-text>
    </v-card>
    <v-snackbar color="red" v-model="snackbar">
      {{ snackbarText }}
      <v-btn text color="white" @click="snackbar = false">close</v-btn>
    </v-snackbar>
  </v-dialog>
</template>

<script>
import instance from "@/services/MainService";
import { validationMixin } from "vuelidate";
export default {
  mixins: [validationMixin],
  name: "add-project",
  data() {
    return {
      form: {
        id: null,
        project_name: "",
        description: "",
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
      dialog: false,
      snackbar: false,
      snackbarText: "",
      nameRules: [
        v => !!v || "Project Name is required",
        v =>
          (v && v.length <= 10) ||
          "Project Name must be less than 10 characters"
      ],
      fileRules: [v => !!v || "It is required to upload a file"],
      linkRules: [
        v => !!v || "It is required to enter the link of Open Data set"
      ]
    };
  },
  methods: {
    uploadFile() {
      console.log(this.file.type);
      this.$store.state.file_uploaded = this.file;
      this.type = this.file.type;
    },
    saveProject() {
      console.log("user id", this.$store.state.user_id);
      this.loading = true;
      var formData = new FormData();
      var project = {
        project_name: this.$store.state.project_name,
        description: this.$store.state.description,
        author: this.$store.state.user,
        user_id: this.$store.state.user_id,
        creation_date: new Date()
      };
      formData.append("project", JSON.stringify(project));
      formData.append("file", this.$store.state.file_uploaded);
      formData.append("user_id", this.$store.state.user_id);
      formData.append("project_name", this.$store.state.project_name);
      formData.append("description", this.$store.state.description);
      formData.append("separator", this.$store.state.csv.separator);
      formData.append("tables", this.$store.state.html.extract_tables);
      formData.append("paragraphs", this.$store.state.html.extract_paragraphs);
      instance
        .post("extract/", formData, {
          headers: {
            "Content-Type": "multipart/form-data",
            Authorization: `JWT ${this.$store.state.jwt}`
          }
        })
        .then(response => {
          console.log(response.data);
          this.project.id = response.data.id;
          this.$store.state.project_id = response.data.project_id;
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
          this.$router.push({ name: "transform" });
        })
        .catch(error => {
          console.log(error);
          console.log(error.response.data.msg);
          this.snackbar = true;
          this.loading = false;
          this.snackbarText = error.response.data.msg;
        });
    },

    newProject() {
      this.project = {};
    }
  }
};
</script>
