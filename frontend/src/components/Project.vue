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
                  >{{ this.project.description }}</v-col>
                </v-row>
                <v-row class="mb-5 pb-2" align-center>
                  <v-col sm="6" cols="6" class="py-0">
                    <h4 class="title font-weight-bold text--primary">
                      <v-icon class="text--primary title font-weight-bold">mdi-account-box</v-icon>Created by :
                    </h4>
                  </v-col>
                  <v-col sm="6" cols="6" class="text-left text--primary subtitle-1 py-0">
                    {{ this.project.author.first_name }}
                    {{this.project.author.last_name}} , {{ this.project.author.email }}
                  </v-col>
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
            <v-card v-if="this.project.input_file !=null" class="mx-auto" max-width="600">
              <v-card-text>
                <p class="display-1 text--primary">Open Data Input file :</p>
                <v-divider></v-divider>
                <v-row class="mb-5 pb-2" align-center>
                  <v-col sm="6" cols="6" class="py-0">
                    <h4 class="title font-weight-bold">
                      <v-icon class="headline mr-2 text--primary">mdi-file</v-icon>File name :
                    </h4>
                  </v-col>
                  <v-col
                    sm="6"
                    cols="6"
                    class="text-left text--primary subtitle-1 py-0"
                  >{{ this.project.input_file.filename }}</v-col>
                </v-row>
                <v-row class="mb-5 pb-2" align-center>
                  <v-col sm="6" cols="6" class="py-0">
                    <h4 class="title font-weight-bold">
                      <v-icon
                        v-if="this.project.input_file.file_type==='text/csv'"
                        class="headline mr-2 text--primary"
                      >mdi-file-table</v-icon>
                      <v-icon
                        v-if="this.project.input_file.file_type==='text/html'"
                        class="headline mr-2 text--primary"
                      >mdi-file-code</v-icon>
                      <v-icon
                        v-if="this.project.input_file.file_type==='text/plain'"
                        class="headline mr-2 text--primary"
                      >mdi-file-document</v-icon>
                      <v-icon
                        v-if="this.project.input_file.file_type==='application/pdf'"
                        class="headline mr-2 text--primary"
                      >mdi-file-pdf</v-icon>
                      <v-icon
                        v-if="this.project.input_file.file_type==='image/jpeg'"
                        class="headline mr-2 text--primary"
                      >mdi-file-image</v-icon>
                      <v-icon
                        v-if="this.project.input_file.file_type==='application/vnd.ms-excel'"
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

                <v-row class="mb-5 pb-2" align-center>
                  <v-col sm="6" cols="6" class="py-0">
                    <h4 class="title font-weight-bold">
                      <v-icon class="headline mr-2 text--primary">mdi-file-find</v-icon>File Path :
                    </h4>
                  </v-col>
                  <v-col
                    sm="6"
                    cols="6"
                    class="text-left text--primary subtitle-1 py-0"
                  >{{ this.project.input_file.path }}</v-col>
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
            <v-card v-if="this.project.converted == true" class="mx-auto" max-width="500">
              <v-card-text>
                <p class="headline text--primary">Linked Data Output file :</p>
                <h4>
                  <v-icon>mdi-file</v-icon>fileRDF
                </h4>
                <v-divider></v-divider>
                <p class="font-weight-bold">
                  The conversion is finished at :
                  {{ this.project.converted_at }}
                </p>
              </v-card-text>
            </v-card>
          </v-tab-item>
        </v-tabs-items>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import Navbar from "@/components/Navbar";
import axios from "axios";
export default {
  components: {
    Navbar
  },
  data: () => {
    return {
      projects: [],
      tab: 0,
      tabs: [
        { name: "Details", icon: "  mdi-file-document" },
        { name: "Source File", icon: " mdi-file-download" },
        { name: "Resulted Files", icon: " mdi-file-move " },
        { name: "Project Parameters", icon: "mdi-file-cog" }
      ],
      converted: false,
      dialogRead: false,
      activeSlide: null,
      project: {}
    };
  },
  methods: {
    seeInputFile() {
      this.tab++;
    },
    seeOutputFile() {
      this.tab = this.tab + 2;
    },
    getProject(id) {
      axios
        .get("http://127.0.0.1:8000/api/projects/" + id)
        .then(response => {
          this.project = response.data;
          console.log(this.project.input_file.filename);
          console.log(this.project.converted);
        })
        .catch(error => console.log(error));
    }
  },
  mounted() {
    this.getProject(this.$route.params.id);
  }
};
</script>