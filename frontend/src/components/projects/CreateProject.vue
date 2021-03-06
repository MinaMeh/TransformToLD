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
            :counter="50"
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
          <v-col class="text-right">
            <v-btn text class="font-weight-bold success" @click="saveProject()" :loading="loading">
              <v-icon>mdi-plus</v-icon>Create
            </v-btn>
          </v-col>
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
import { validationMixin } from "vuelidate";
import operations from "@/services/OperationsService";
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
          (v && v.length <= 255) ||
          "Project Name must be less than 255 characters"
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
      operations
        .extract(this.$store)
        .then(response => {
          console.log(response);
          this.loading = false;
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
