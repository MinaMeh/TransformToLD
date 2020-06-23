<template>
  <v-container fluid>
    <v-row>
      <v-col>
        <horizontal-stepper
          top-buttons
          :steps="demoSteps"
          @completed-step="completeStep"
          @active-step="isStepActive"
          @stepper-finished="alert"
          @before-next-step="beforeNextStep"
          @clicking-back="$store.state.progress=false"
        ></horizontal-stepper>
      </v-col>
    </v-row>
  </v-container>
</template>
<script>
import HorizontalStepper from "vue-stepper";
import axios from "axios";

// This components will have the content for each stepper step.
import CreateComponent from "./CreateComponent";
import PreprocessComponent from "./PreprocessComponent";
import VocabsComponent from "./VocabsComponent";
import ConvertComponent from "./ConvertComponent.vue";
import ExploreComponent from "./ExploreComponent.vue";
import DocumentComponent from "./DocumentComponent.vue";
import ExtractComponent from "./ExtractComponent";
export default {
  components: {
    HorizontalStepper
  },
  data() {
    return {
      demoSteps: [
        {
          icon: "folder",
          name: "first",
          title: "Create",
          subtitle: "Project Creation",
          component: CreateComponent,
          completed: false
        },

        {
          icon: "data_usage",
          name: "second",
          title: "Extract",
          subtitle: "Data Extraction",
          component: ExtractComponent,
          completed: false
        },
        {
          icon: "perm_data_setting",
          name: "third",
          title: "Preprocess",
          subtitle: "Data Preprocessing",
          component: PreprocessComponent,
          completed: false
        },
        {
          icon: "find_in_page",
          name: "fourth",
          title: "Select",
          subtitle: "Vocabularies Selection",
          component: VocabsComponent,
          completed: false
        },
        {
          icon: "explore",
          name: "fifth",
          title: "Explore",
          subtitle: "Data Exploration and mapping",
          component: ExploreComponent,
          completed: false
        },
        {
          icon: "transform",
          name: "sixth",
          title: "Convert",
          subtitle: "Data Conversion to RDF",
          component: ConvertComponent,
          completed: false
        },

        {
          icon: "info",
          name: "seventh",
          title: "Document",
          subtitle: "Data Documentation",
          component: DocumentComponent,
          completed: false
        }
      ]
    };
  },
  methods: {
    // Executed when @completed-step event is triggered
    completeStep(payload) {
      this.demoSteps.forEach(step => {
        if (step.name === payload.name) {
          step.completed = true;
        }
      });
    },
    // Executed when @active-step event is triggered
    isStepActive(payload) {
      this.demoSteps.forEach(step => {
        if (step.name === payload.name) {
          if (step.completed === true) {
            step.completed = false;
          }
        }
      });
    },
    beforeNextStep({ currentStep }, next) {
      this.$store.state.progress = true;

      if (currentStep.name == "first") {
        var formData = new FormData();
        var project = {
          project_name: this.$store.state.project_name,
          author: this.$store.state.user
        };
        formData.append("project", JSON.stringify(project));
        formData.append("file", this.$store.state.file_uploaded);
        formData.append("project_name", this.$store.state.project_name);
        formData.append("separator", this.$store.state.csv.separator);
        formData.append("tables", this.$store.state.html.extract_tables);
        formData.append(
          "paragraphs",
          this.$store.state.html.extract_paragraphs
        );

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
              this.$store.state.text.paragraph =
                response.data.results.paragraph;
              this.$store.state.text.sentences =
                response.data.results.sentences;
            }

            this.$store.state.progress = false;
          })
          .catch(error => console.log(error));
      }
      if (currentStep.name == "second") {
        this.$store.state.progress = true;

        var formData_2 = new FormData();

        formData_2.append("file_type", this.$store.state.file_type);

        if (this.$store.state.file_type == "csv") {
          formData_2.append(
            "columns",
            JSON.stringify(this.$store.state.csv.headers)
          );
        }

        if (this.$store.state.file_type == "html") {
          formData_2.append(
            "tables",
            JSON.stringify(this.$store.state.html.tables)
          );
          formData_2.append(
            "paragraphs",
            JSON.stringify(this.$store.state.html.paragraphs)
          );
        }
        if (this.$store.state.file_type == "text") {
          formData_2.append(
            "paragraph",
            JSON.stringify(this.$store.state.text)
          );
        }

        axios
          .post("http://localhost:8000/preprocess/", formData_2)
          .then(response => {
            console.log(response.data);
            console.log("before", this.$store.state.progress);
            this.$store.state.progress = false;
            console.log("after", this.$store.state.progress);

            if (this.$store.state.file_type == "csv") {
              this.$store.state.csv.headers = response.data.headers;
            }
            if (this.$store.state.file_type == "html") {
              this.$store.state.html.tables = response.data.tables_selected;
              this.$store.state.html.paragraphs =
                response.data.paragraphs_selected;
            }
            if (this.$store.state.file_type == "text") {
              this.$store.state.text.paragraph = response.data;
            }
          })
          .catch();
      }
      if (currentStep.name == "fourth") {
        this.$store.state.progress = true;

        var formData3 = new FormData();
        formData3.append("file_type", this.$store.state.file_type);
        formData3.append("vocabs", JSON.stringify(this.$store.state.vocabs));

        if (this.$store.state.file_type == "csv") {
          formData3.append(
            "columns",
            JSON.stringify(this.$store.state.csv.headers)
          );
        }
        if (this.$store.state.file_type == "html") {
          formData3.append(
            "tables",
            JSON.stringify(this.$store.state.html.tables)
          );
          formData3.append(
            "paragraphs",
            JSON.stringify(this.$store.state.html.paragraphs)
          );
        }
        if (this.$store.state.file_type == "text") {
          formData3.append(
            "paragraph",
            JSON.stringify(this.$store.state.text.paragraph)
          );
        }

        axios
          .post("http://localhost:8000/explore/", formData3)
          .then(response => {
            console.log(response.data);
            if (this.$store.state.file_type == "csv") {
              this.$store.state.csv.terms = response.data.terms;
              console.log(response.data);
            }
            if (this.$store.state.file_type == "html") {
              this.$store.state.html.tables = response.data.tables;
              this.$store.state.html.paragraphs = response.data.paragraphs;
            }
            if (this.$store.state.file_type == "text") {
              this.$store.state.text.paragraph = response.data;
            }

            this.$store.state.progress = false;
          })
          .catch();
      }
      if (currentStep.name == "fifth") {
        var formData4 = new FormData();
        formData4.append("file_type", this.$store.state.file_type);
        formData4.append("file_name", this.$store.state.filename);
        if (this.$store.state.file_type == "csv") {
          formData4.append("delimiter", this.$store.state.csv.separator);
          var terms = [];
          this.$store.state.csv.terms.forEach(function(term) {
            terms.push({ property: term.property, term: term.selected });
          });
          formData4.append("terms", JSON.stringify(terms));
        }
        if (this.$store.state.file_type == "text") {
          var triplets = [];
          this.$store.state.text.paragraph.sentences.forEach(function(
            sentence
          ) {
            sentence.triplets.forEach(function(triplet) {
              if (triplet.selected) {
                triplets.push(triplet);
              }
            });
          });
          terms = [];
          this.$store.state.text.paragraph.terms.forEach(function(term) {
            terms.push({ property: term.property, term: term.selected });
          });
          formData4.append("terms", JSON.stringify(terms));
          formData4.append("triplets", JSON.stringify(triplets));
        }
        if (this.$store.state.file_type == "html") {
          var tables = [];
          this.$store.state.html.tables.forEach(function(table) {
            if (table.selected) {
              var filename = table.filename;
              var id = table.id;
              var terms = [];
              table.terms.forEach(function(term) {
                terms.push({ property: term.property, term: term.selected });
              });
              tables.push({ filename: filename, id: id, terms: terms });
            }
          });
          var paragraphs = [];
          this.$store.state.html.paragraphs.forEach(function(paragraph) {
            if (paragraph.selected) {
              var id = paragraph.id;
              var terms = [];
              var triplets = [];
              paragraph.terms.forEach(function(term) {
                terms.push({ property: term.property, term: term.selected });
              });
              paragraph.sentences.forEach(function(sentence) {
                sentence.triplets.forEach(function(triplet) {
                  if (triplet.selected) triplets.push(triplet);
                });
              });

              paragraphs.push({ id: id, terms: terms, triplets: triplets });
            }
          });

          formData4.append("tables", JSON.stringify(tables));
          formData4.append("paragraphs", JSON.stringify(paragraphs));
        }
        axios
          .post("http://localhost:8000/convert/", formData4)
          .then(response => {
            this.$store.state.progress = false;
            console.log(response.data);
            if (this.$store.state.file_type == "csv") {
              this.$store.state.csv.triplets = response.data;
            }
            if (this.$store.state.file_type == "text") {
              this.$store.state.text.triplets = response.data;
            }
            if (this.$store.state.file_type == "html") {
              this.$store.state.html.tables_triplets = response.data.tables;
              this.$store.state.html.paragraphs_triplets =
                response.data.paragraphs;
            }
          })
          .catch();
      }
      next();
    },
    alert() {
      alert("finished");
    }
  }
};
</script>