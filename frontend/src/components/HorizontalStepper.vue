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
        ></horizontal-stepper>
      </v-col>
    </v-row>
  </v-container>
</template>
<script>
import HorizontalStepper from "vue-stepper";
import axios from "axios";

// This components will have the content for each stepper step.
import CollectComponent from "./CollectComponent.vue";
import PreprocessComponent from "./PreprocessComponent";

import ConvertComponent from "./ConvertComponent.vue";
import ExploreComponent from "./ExploreComponent.vue";
import DocumentComponent from "./DocumentComponent.vue";
import LinkComponent from "./LinkComponent";
export default {
  components: {
    HorizontalStepper
  },
  data() {
    return {
      demoSteps: [
        {
          icon: "get_app",
          name: "first",
          title: "Collect",
          subtitle: "Data Collection and selecting vocabularies",
          component: CollectComponent,
          completed: false
        },

        {
          icon: "perm_data_setting",
          name: "second",
          title: "Preprocess",
          subtitle: "Data Preprocessing",
          component: PreprocessComponent,
          completed: false
        },
        {
          icon: "explore",
          name: "third",
          title: "Explore",
          subtitle: "Data Exploration and mapping",
          component: ExploreComponent,
          completed: false
        },
        {
          icon: "transform",
          name: "fourth",
          title: "Convert",
          subtitle: "Data Conversion to RDF",
          component: ConvertComponent,
          completed: false
        },

        {
          icon: "link",
          name: "fifth",
          title: "Link",
          subtitle: "Data Linking",
          component: LinkComponent,
          completed: false
        },
        {
          icon: "info",
          name: "sixth",
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
      if (currentStep.name == "first") {
        let formData = new FormData();
        formData.append("file", this.$store.state.file_uploaded);
        formData.append("vocabs", this.$store.state.vocabs);
        axios
          .post("http://localhost:8000/preprocess/", formData, {
            headers: {
              "Content-Type": "multipart/form-data"
            }
          })
          .then(response => {
            this.$store.state.file_content = response.data;
            console.log(response.data);
          })
          .catch(error => console.log(error));
      }
      if (currentStep.name == "second") {
        console.log("columns" + typeof this.$store.state.csv.columns);
        let formData = new FormData();
        formData.append("columns", this.$store.state.csv.columns);
        formData.append("list_vocabs", this.$store.state.vocabs);
        formData.append("file_type", "csv");

        axios
          .post("http://localhost:8000/explore/", formData)
          .then(response => {
            console.log(response.data);
            this.$store.state.csv.terms = response.data.results;
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