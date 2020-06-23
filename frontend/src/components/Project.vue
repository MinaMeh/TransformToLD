<template>
  <v-container class="px-5 py-5" fluid>
    <h1 class="font-weight-bold display-1">Project "{{projects[1].project_name}}" Details</h1>
    <v-divider></v-divider>
    <v-card>
      <v-row wrap>
        <v-col grow class="py-1 elevation-2">
          <v-tabs v-model="tab" show-arrows grow class="fill-width" height="60px">
            <v-tabs-slider color="primary"></v-tabs-slider>
            <v-tab v-for="t in tabs" :key="t">
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
                    <v-col sm="6" cols="6" class="text-left text--primary subtitle-1 py-0">Test</v-col>
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
                    >Test Description</v-col>
                  </v-row>
                  <v-row class="mb-5 pb-2" align-center>
                    <v-col sm="6" cols="6" class="py-0">
                      <h4 class="title font-weight-bold text--primary">
                        <v-icon class="text--primary title font-weight-bold">mdi-file-certificate</v-icon>Licence :
                      </h4>
                    </v-col>
                    <v-col
                      sm="6"
                      cols="6"
                      class="text-left text--primary subtitle-1 py-0"
                    >licence exemple</v-col>
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
                    >MEKIDECHE Imene</v-col>
                  </v-row>
                  <v-row class="mb-5 pb-2" align-center>
                    <v-col sm="6" cols="6" class="py-0">
                      <h4 class="title font-weight-bold text--primary">
                        <v-icon class="text--primary title font-weight-bold">mdi-calendar</v-icon>Creation date :
                      </h4>
                    </v-col>
                    <v-col sm="6" cols="6" class="text-left text--primary subtitle-1 py-0">Today</v-col>
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
                      <v-btn
                        @click="seeOutputFile ()"
                        text
                        color="primary"
                      >See results of conversion</v-btn>
                    </v-col>
                  </v-row>
                  <v-row class="mb-5 pb-2" align-center>
                    <v-col sm="6" cols="6" class="py-0">
                      <h4 class="title font-weight-bold text--primary">
                        <v-icon class="text--primary title font-weight-bold">mdi-file-edit</v-icon>Edition historical :
                      </h4>
                    </v-col>
                    <v-col sm="6" cols="6" class="text-left text--primary subtitle-1 py-0">
                      <v-btn
                        style="{ cursor: 'pointer'}"
                        text
                        color="primary"
                        @click="seeEditions()"
                      >See historic of editions</v-btn>
                    </v-col>
                  </v-row>
                </v-card-text>
              </v-card>
            </v-tab-item>
            <v-tab-item>
              <v-card class="mx-auto" max-width="500">
                <v-card-text>
                  <p class="headline text--primary">Open Data Input file :</p>
                  <h4>
                    <v-icon>mdi-file</v-icon>
                    {{projects[1].inputFile}}
                  </h4>
                  <v-divider></v-divider>
                  <p class="font-weight-bold">Uploaded {{projects[1].creation_date}}</p>
                </v-card-text>
              </v-card>
            </v-tab-item>
            <v-tab-item>
              <v-card v-if="converted==false" class="mx-auto" max-width="500">
                <v-card-text>
                  <p
                    class="text-center font-weight-bold red--text"
                  >The input Dataset is not converted yet !</p>
                </v-card-text>
              </v-card>
              <v-card v-if="converted==true" class="mx-auto" max-width="500">
                <v-card-text>
                  <p class="headline text--primary">Linked Data Output file :</p>
                  <h4>
                    <v-icon>mdi-file</v-icon>fileRDF
                  </h4>
                  <v-divider></v-divider>
                  <p class="font-weight-bold">The conversion is finished {{dateConvertion}}</p>
                </v-card-text>
              </v-card>
            </v-tab-item>
          </v-tabs-items>
        </v-col>
      </v-row>
      <v-dialog v-model="dialogRead" width="500">
        <v-card>
          <v-card-title class="headline elevation-1" primary-title>Editions</v-card-title>
          <v-card-text class="pa-5">list des editions</v-card-text>
          <v-card-actions class="pa-5">
            <v-btn class="ml-auto" @click="dialogRead=false" color="error">Close</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-card>
  </v-container>
</template>

<script>
const allProjects = [
  {
    id: 1,
    project_name: "projet test",
    description: "from open to linked :D",
    licence: "MIT Licence ex",
    author: " MEKIDECHE Imene",
    creation_date: "Today, 9:18AM",
    updated: false,
    inputFile: "File.txt"
  },

  {
    id: 2,
    project_name: "projet test 2",
    description: "from open to linked :D",
    licence: "MIT Licence ex",
    author: " MEHERHERA Amina",
    creation_date: "3 Days Ago",
    updated: false,
    inputFile: "File.csv"
  }
];
export default {
  data: () => {
    return {
      projects: [...allProjects],
      tab: 0,
      tabs: [
        { name: "Details", icon: "  mdi-file-document" },
        { name: "Source File", icon: " mdi-file-download" },
        { name: "Resulted Files", icon: " mdi-file-move " },
        { name: "Project Parameters", icon: "mdi-file-cog" }
      ],
      converted: false,
      dialogRead: false,
      activeSlide: null
    };
  },
  created() {
    this.allProjects = allProjects;
  },
  methods: {
    seeEditions() {
      this.dialogRead = true;
    },
    seeInputFile() {
      this.tab++;
    },
    seeOutputFile() {
      this.tab = this.tab + 2;
    }
  }
};
</script>