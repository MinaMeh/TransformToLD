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
        <v-snackbar v-model="error" color="red">
          {{errorMsg}}
          <v-btn text @click="error=false">close</v-btn>
        </v-snackbar>
      </v-col>
      <ChooseFormat v-if="modal" :chooseOutput="modal" @convert="convert" @close="modal=false"></ChooseFormat>
    </v-row>
  </v-container>
</template>
<script>
import HorizontalStepper from "vue-stepper";
import ChooseFormat from "@/components/modals/ChooseFormat";
import operations from "@/services/OperationsService";

// This components will have the content for each stepper step.
import PreprocessComponent from "./PreprocessComponent";
import VocabsComponent from "./VocabsComponent";
import ConvertComponent from "./ConvertComponent.vue";
import ExploreComponent from "./ExploreComponent.vue";
import DocumentComponent from "./DocumentComponent.vue";
import ExtractComponent from "./ExtractComponent";

export default {
  components: {
    HorizontalStepper,
    ChooseFormat
  },
  data() {
    return {
      error: false,
      errorMsg: "",
      selectedFormat: "",
      modal: false,
      demoSteps: [
        {
          icon: "data_usage",
          name: "first",
          title: "Extract",
          subtitle: "Data Extraction",
          component: ExtractComponent,
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
          icon: "find_in_page",
          name: "third",
          title: "Select",
          subtitle: "Vocabularies Selection",
          component: VocabsComponent,
          completed: false
        },
        {
          icon: "explore",
          name: "fourth",
          title: "Explore",
          subtitle: "Data Exploration and mapping",
          component: ExploreComponent,
          completed: false
        },
        {
          icon: "transform",
          name: "fifth",
          title: "Convert",
          subtitle: "Data Conversion to RDF",
          component: ConvertComponent,
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
      console.log("progress", this.$store.state.progress);
      if (currentStep.name == "first") {
        this.$store.state.progress = true;

        operations
          .preprocess(this.$store)
          .then(response => {
            console.log(response);
            this.$store.state.progress = false;
            next();
          })
          .catch(error => {
            console.log(error);
            this.error = true;
            this.errorMsg = error.response.data.msg;
            this.$store.state.progress = false;
          });
      }
      if (currentStep.name == "second") {
        this.$store.state.progress = false;

        next();
      }

      if (currentStep.name == "third") {
        this.$store.state.progress = true;

        operations
          .explore(this.$store)
          .then(response => {
            console.log(response);
            this.$store.state.progress = false;

            next();
          })
          .catch(error => {
            console.log(error);
            this.$store.state.progress = false;

            this.error = true;
            this.errorMsg = error.response.data.msg;
          });
      }
      if (currentStep.name == "fourth") {
        this.$store.state.progress = true;

        operations
          .convert(this.$store)
          .then(response => {
            console.log(response);
            this.$store.state.progress = false;

            next();
          })
          .catch(error => {
            console.log(error);
            this.error = true;
            this.errorMsg = error.response.data.msg;
            this.$store.state.progress = false;
          });
      }
      if (currentStep.name == "fifth") {
        next();
      }
      if (currentStep.name == "sixth") {
        this.modal = true;
      }
    },
    alert() {
      alert("finished");
    },
    convert(format) {
      operations
        .document(this.$store, format)
        .then(response => {
          console.log(response.data);
          this.$store.state.progress = false;

          this.$router.push("/projects/" + this.$store.state.project_id);
        })
        .catch(error => {
          console.log(error);
          this.$store.state.progress = false;
        });
    }
  }
};
</script>