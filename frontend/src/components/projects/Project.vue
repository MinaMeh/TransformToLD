<template>
  <v-container class="px-5 py-5" fluid>
    <Navbar></Navbar>
    <h1 class="font-weight-bold display-1">Project "{{ this.project.project_name }}" Details</h1>
    <v-divider></v-divider>

    <v-row wrap>
      <v-col grow class="py-1 elevation-2">
        <v-tabs v-model="tab" show-arrows grow class="fill-width" height="60px">
          <v-tabs-slider color="primary"></v-tabs-slider>
          <v-tab v-for="(t, index) in tabs" :key="index">
            <div class="body-2 font-weight-bold py-1">
              {{ t.name }}
              <v-icon v-text="t.icon"></v-icon>
            </div>
          </v-tab>
        </v-tabs>
        <v-tabs-items v-model="tab" grow class="pa-4">
          <v-tab-item>
            <v-card class="mx-auto" max-width="600">
              <v-card-text>
                <v-row class="mb-5 pb-2" align-center>
                  <v-col sm="6" cols="6" class="py-0">
                    <h4 class="title font-weight-bold text--primary">
                      <v-icon class="text--primary title font-weight-bold">mdi-file</v-icon>Project Name :
                    </h4>
                  </v-col>
                  <v-col
                    sm="6"
                    cols="6"
                    class="text-left text--primary subtitle-1 py-0"
                  >{{ this.project.project_name }}</v-col>
                </v-row>
                <v-row class="mb-5 pb-2" align-center>
                  <v-col sm="6" cols="6" class="py-0">
                    <h4 class="title font-weight-bold text--primary">
                      <v-icon class="text--primary title font-weight-bold">mdi-file-document-edit</v-icon>Description :
                    </h4>
                  </v-col>
                  <v-col
                    sm="6"
                    cols="6"
                    class="text-left text--primary subtitle-1 py-0"
                  >{{ this.project.metadata.description }}</v-col>
                </v-row>
                <v-row class="mb-5 pb-2" align-center>
                  <v-col sm="6" cols="6" class="py-0">
                    <h4 class="title font-weight-bold text--primary">
                      <v-icon class="text--primary title font-weight-bold">mdi-account-box</v-icon>Created by :
                    </h4>
                  </v-col>
                  <v-col
                    sm="6"
                    cols="6"
                    class="text-left text--primary subtitle-1 py-0"
                  >{{ this.project.metadata.creator }}</v-col>
                </v-row>
                <v-row class="mb-5 pb-2" align-center>
                  <v-col sm="6" cols="6" class="py-0">
                    <h4 class="title font-weight-bold text--primary">
                      <v-icon class="text--primary title font-weight-bold">mdi-calendar</v-icon>Creation date :
                    </h4>
                  </v-col>
                  <v-col
                    sm="6"
                    cols="6"
                    class="text-left text--primary subtitle-1 py-0"
                  >{{ this.project.creation_date | formatDate }}</v-col>
                </v-row>
                <v-row class="mb-5 pb-2" align-center>
                  <v-col sm="6" cols="6" class="py-0">
                    <h4 class="title font-weight-bold text--primary">
                      <v-icon class="text--primary title font-weight-bold">mdi-file-download</v-icon>Open Data input :
                    </h4>
                  </v-col>
                  <v-col sm="6" cols="6" class="text-left text--primary subtitle-1 py-0">
                    <v-btn @click="seeInputFile()" text color="primary">See input dataset</v-btn>
                  </v-col>
                </v-row>
                <v-row class="mb-5 pb-2" align-center>
                  <v-col sm="6" cols="6" class="py-0">
                    <h4 class="title font-weight-bold text--primary">
                      <v-icon class="text--primary title font-weight-bold">mdi-file-download</v-icon>Linked Data output :
                    </h4>
                  </v-col>
                  <v-col sm="6" cols="6" class="text-left text--primary subtitle-1 py-0">
                    <v-btn @click="seeOutputFile()" text color="primary">See results of conversion</v-btn>
                  </v-col>
                </v-row>
              </v-card-text>
            </v-card>
          </v-tab-item>
          <v-tab-item>
            <v-card v-if="this.project.input_file === null" class="mx-auto" max-width="500">
              <v-card-text>
                <p class="text-center font-weight-bold red--text">No file has been uploaded !</p>
              </v-card-text>
            </v-card>
            <v-card v-if="this.project.input_file != null" class="mx-auto" max-width="600">
              <v-card-text>
                <p class="display-1 text--primary">Open Data Input file :</p>
                <v-divider></v-divider>
                <v-row class="mb-5 pb-2" align-center>
                  <v-col sm="6" cols="6" class="py-0">
                    <h4 class="title font-weight-bold">
                      <v-icon class="headline mr-2 text--primary">mdi-file</v-icon>File name :
                    </h4>
                  </v-col>
                  <v-col sm="6" cols="6" class="text-left text--primary subtitle-1 py-0">
                    <a
                      @click.prevent="getFile(project.input_file)"
                    >{{ this.project.input_file.filename }}</a>
                  </v-col>
                </v-row>
                <v-row class="mb-5 pb-2" align-center>
                  <v-col sm="6" cols="6" class="py-0">
                    <h4 class="title font-weight-bold">
                      <v-icon
                        v-if="this.project.input_file.file_type === 'text/csv'"
                        class="headline mr-2 text--primary"
                      >mdi-file-table</v-icon>
                      <v-icon
                        v-if="this.project.input_file.file_type === 'text/html'"
                        class="headline mr-2 text--primary"
                      >mdi-file-code</v-icon>
                      <v-icon
                        v-if="
                          this.project.input_file.file_type === 'text/plain'
                        "
                        class="headline mr-2 text--primary"
                      >mdi-file-document</v-icon>
                      <v-icon
                        v-if="
                          this.project.input_file.file_type ===
                            'application/pdf'
                        "
                        class="headline mr-2 text--primary"
                      >mdi-file-pdf</v-icon>
                      <v-icon
                        v-if="
                          this.project.input_file.file_type === 'image/jpeg'
                        "
                        class="headline mr-2 text--primary"
                      >mdi-file-image</v-icon>
                      <v-icon
                        v-if="
                          this.project.input_file.file_type ===
                            'application/vnd.ms-excel'
                        "
                        class="headline mr-2 text--primary"
                      >mdi-file-excel</v-icon>File Type :
                    </h4>
                  </v-col>
                  <v-col
                    sm="6"
                    cols="6"
                    class="text-left text--primary subtitle-1 py-0"
                  >{{ this.project.input_file.file_type }}</v-col>
                </v-row>
              </v-card-text>
            </v-card>
          </v-tab-item>
          <v-tab-item>
            <v-card v-if="this.project.converted == false" class="mx-auto" max-width="500">
              <v-card-text>
                <p
                  class="text-center font-weight-bold red--text"
                >The input Dataset is not converted yet !</p>
              </v-card-text>
            </v-card>
            <v-card v-if="this.project.converted == true" class="mx-auto">
              <p class="headline text--primary">Linked Data Output file :</p>

              <v-card-text>
                <v-data-table :headers="headers" :items="project.output_files">
                  <template v-slot:item.created_at="{ item }">{{item.created_at |formatDate}}</template>
                  <template v-slot:item.filename="{ item }">
                    <a @click.prevent="getFile(item)">{{ item.filename }}</a>
                  </template>
                </v-data-table>
              </v-card-text>
              <v-card-actions>
                <v-btn color="primary" @click="chooseOutput=true">Convert to another format</v-btn>
              </v-card-actions>
            </v-card>
            <ChooseFormat
              v-if="chooseOutput"
              :chooseOutput="chooseOutput"
              @convert="convert"
              @close="close()"
            ></ChooseFormat>
          </v-tab-item>
          <v-tab-item>
            <CsvComponent
              v-if="this.project.csv_data!=null"
              :vocabularies="this.project.vocabularies"
              :headers="this.project.csv_data.headers"
              :triplets="this.project.triplets"
              @editTerm="editCsvTerm"
            ></CsvComponent>
            <TextComponent
              v-if="this.project.text_data!=null"
              :vocabularies="this.project.vocabularies"
              :terms="this.project.terms"
              :triplets="this.project.triplets"
            ></TextComponent>
            <HtmlComponent :v-if="this.project.html_data!=null" :project="this.project"></HtmlComponent>
          </v-tab-item>
        </v-tabs-items>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import Navbar from "@/components/Navbar";
import CsvComponent from "@/components/show/CsvComponent";
import TextComponent from "@/components/show/TextComponent";
import HtmlComponent from "@/components/show/HtmlComponent";
import ChooseFormat from "@/components/modals/ChooseFormat";
import instance from "@/services/MainService";
export default {
  components: {
    Navbar,
    CsvComponent,
    TextComponent,
    HtmlComponent,
    ChooseFormat,
  },
  data: () => {
    return {
      projects: [],
      tab: 0,
      chooseOutput: false,
      tabs: [
        { name: "Details", icon: "  mdi-file-document" },
        { name: "Source File", icon: " mdi-file-download" },
        { name: "Resulted Files", icon: " mdi-file-move " },
        { name: "Project Parameters", icon: "mdi-file-cog" },
      ],
      headers: [
        { text: "File", value: "filename" },
        { text: "Format", value: "file_type" },
        { text: "Creation date", value: "created_at" },
      ],

      converted: false,
      dialogRead: false,
      activeSlide: null,
      project: {
        author: {
          first_name: "",
          last_name: "",
          email: "",
        },
      },
    };
  },
  methods: {
    seeInputFile() {
      this.tab++;
    },
    seeOutputFile() {
      this.tab = this.tab + 2;
    },
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
    getProject(id) {
      instance
        .get("api/projects/" + id, {
          headers: {
            "Content-Type": "multipart/form-data",
            Authorization: `JWT ${this.$store.state.jwt}`,
          },
        })
        .then((response) => {
          this.project = response.data.project;
          this.project.triplets = response.data.triplets;
          this.project.terms = response.data.terms;
          if (this.project.vocabularies.length == 0) {
            this.project.vocabularies = response.data.vocabularies;
          }
          console.log(this.project.input_file.filename);
          console.log(this.project.converted);
        })
        .catch((error) => console.log(error));
    },
    convert(value) {
      var formdata = new FormData();
      formdata.append("project_id", this.project.id);
      formdata.append("format", value);
      instance
        .post("translate/", formdata)
        .then((response) => {
          console.log(response.data);
          this.close();
          this.getProject(this.$route.params.id);
        })
        .catch((error) => {
          console.log(error);
        });
      console.log(value);
    },
    close() {
      this.chooseOutput = false;
    },
    editCsvTerm(value) {
      this.project.csv_data.headers.forEach((term) => {
        if (term.name == value.name) {
          term.term = value.term;
        }
      });
    },
  },
  mounted() {
    this.getProject(this.$route.params.id);
  },
};
</script>
