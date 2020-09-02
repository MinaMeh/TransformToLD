<template>
  <v-dialog max-width="900px" v-model="dialog">
    <v-card>
      <v-card-title class="font-weight-bold text--primary">Convert Dataset</v-card-title>
      <v-divider></v-divider>
      <v-card-text>
        <v-form class="px-3">
          <v-text-field
            outlined
            label="Dataset Title"
            v-model="$store.state.metadata.title"
            placeholder="Enter the title of your dataset"
            prepend-icon="mdi-file"
          ></v-text-field>

          <v-text-field
            outlined
            label="Creator"
            v-model="$store.state.metadata.creator "
            placeholder="Enter creator of your dataset"
            prepend-icon="mdi-file"
          ></v-text-field>
          <v-text-field
            outlined
            label="License"
            v-model="$store.state.metadata.license"
            prepend-icon="mdi-file"
          ></v-text-field>
          <v-text-field
            outlined
            label="Subject"
            v-model="$store.state.metadata.subject"
            prepend-icon="mdi-file"
          ></v-text-field>
          <v-textarea
            counter
            outlined
            label="Description of your dataset"
            v-model="$store.state.metadata.description"
            placeholder="Describe your data set"
            prepend-icon="mdi-file-document-edit"
          ></v-textarea>

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
          <v-col cols="12">
            <v-select
              outlined
              v-model="selectedFormat"
              label="Select an output format"
              :items="outputFormat"
              item-value="value"
              item-text="text"
            ></v-select>
          </v-col>
          <v-spacer></v-spacer>
          <v-col class="text-right">
            <v-btn text class="font-weight-bold error mr-5" @click="$emit('close')">
              <v-icon>mdi-minus</v-icon>Close
            </v-btn>

            <v-btn text class="font-weight-bold success" @click="auto_convert()" :loading="loading">
              <v-icon>mdi-plus</v-icon>Convert
            </v-btn>
          </v-col>
        </v-form>
        <v-col cols="12">
          {{step}}
          <span v-if="step=='Dataset converti'">
            <a @click.prevent="getFile(output_file)">Download converted dataset</a>
          </span>
        </v-col>
        <v-col cols="12">
          <v-progress-linear height="10" striped :value="value"></v-progress-linear>
        </v-col>
      </v-card-text>
    </v-card>
    <v-snackbar color="red" v-model="snackbar">
      {{ snackbarText }}
      <v-btn text color="white" @click="snackbar = false">close</v-btn>
    </v-snackbar>
  </v-dialog>
</template>

<script>
import operations from "@/services/OperationsService";
import instance from "@/services/MainService";
import { validationMixin } from "vuelidate";
export default {
  mixins: [validationMixin],
  props: ["dialog"],
  data() {
    return {
      output_file: "",
      outputFormat: [
        { text: "Turtle", value: "turtle" },
        { text: "XML", value: "xml" },
        { text: "JSON-LD", value: "json-ld" },
        { text: "N3", value: "n3" },
        { text: "NT", value: "nt" },
        { text: "NQUADS", value: "nquads" },
        { text: "Trix", value: "trix" },
        { text: "Trig", value: "trig" },
      ],
      selectedFormat: "",

      value: 0,
      step: "",
      form: {
        id: null,
        description: "",
        file_link: "",
      },
      html: {
        tables: true,
        paragraphs: true,
      },
      link: false,
      file: null,
      type: null,
      filename: "No file uploaded",
      csv: {
        separator: ";",
      },
      loading: false,
      snackbar: false,
      snackbarText: "",
      nameRules: [
        (v) => !!v || "Project Name is required",
        (v) =>
          (v && v.length <= 255) ||
          "Project Name must be less than 255 characters",
      ],
      fileRules: [(v) => !!v || "It is required to upload a file"],
      linkRules: [
        (v) => !!v || "It is required to enter the link of Open Data set",
      ],
    };
  },
  methods: {
    getFile(file) {
      console.log(file);
      instance
        .get("getFile", {
          params: {
            file_path: file.path,
          },
        })
        .then((response) => {
          var data = [];
          if (Array.isArray(response.data)) {
            response.data.forEach((element) => {
              data.push(element);
            });
            data = JSON.stringify(data);
            console.log(data);
          } else {
            data = response.data;
          }
          var fileURL = window.URL.createObjectURL(new Blob([data]));
          var fileLink = document.createElement("a");

          fileLink.href = fileURL;
          fileLink.setAttribute("download", file.filename);
          document.body.appendChild(fileLink);

          fileLink.click();
        });
    },

    uploadFile() {
      console.log(this.file.type);
      this.$store.state.file_uploaded = this.file;
      this.type = this.file.type;
    },
    auto_convert() {
      this.$store.state.project_name = "automatic";
      this.$store.state.description = "";
      this.step = "Extraction";
      this.value = 0;
      this.$store.state.user = {
        email: "test@test.com",
        first_name: "test",
        last_name: "test",
      };
      this.$store.state.user_id = 0;
      this.step = "Extraction";
      operations
        .extract(this.$store)
        .then((response) => {
          console.log(response);
          this.value = (1 / 5) * 100;
          this.step = "Prétraitement";

          operations
            .preprocess(this.$store)
            .then((response) => {
              console.log(response);
              this.value = (2 / 5) * 100;
              this.step = "Alignement";

              operations
                .explore(this.$store)
                .then((response) => {
                  console.log(response);
                  this.value = (3 / 5) * 100;
                  this.step = "Conversion";

                  operations
                    .convert(this.$store)
                    .then((response) => {
                      console.log(response);
                      this.value = (4 / 5) * 100;
                      this.step = "Docuementation";
                      operations
                        .document(this.$store, this.selectedFormat)
                        .then((response) => {
                          console.log(response.data);
                          this.value = 100;
                          this.step = "Dataset converti";
                          this.output_file =
                            response.data.project.output_files[0];
                        })
                        .catch((error) => {
                          console.log(error);
                        });
                    })
                    .catch((error) => {
                      console.log(error);
                    });
                })
                .catch((error) => {
                  console.log(error);
                });
            })
            .catch((error) => {
              console.log(error);
            });
        })
        .catch((error) => {
          console.log(error);
          console.log(error.response.data.msg);
        });
    },

    newProject() {
      this.project = {};
    },
  },
};
</script>
