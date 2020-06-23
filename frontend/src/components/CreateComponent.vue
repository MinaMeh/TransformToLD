<template>
  <v-container>
    <v-row align="center" justify="center">
      <v-col cols="8">
        <v-form>
          <v-row class="mt-10">
            <v-col cols="12">
              <v-text-field
                outlined
                label="Project"
                placeholder="Project Name"
                v-model="$store.state.project_name"
                prepend-icon="mdi-folder"
              ></v-text-field>
            </v-col>
            <v-col cols="11" v-if="!link">
              <v-file-input
                outlined
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
        </v-form>
      </v-col>
    </v-row>
  </v-container>
</template>
<script>
import { validationMixin } from "vuelidate";
export default {
  props: ["clickedNext", "currentStep"],
  mixins: [validationMixin],
  data() {
    return {
      form: {
        project_name: "",
        file_link: ""
      },
      html: {
        tables: true,
        paragraphs: true
      },
      continue: true,
      link: false,
      file: null,
      filename: "No file uploaded",
      type: null,
      csv: {
        separator: ";"
      }
    };
  },
  computed: {
    project: {
      get() {
        return this.$store.state.project_name;
      },
      set(value) {
        this.$store.state.project_name = value;
      }
    }
  },

  methods: {
    uploadFile() {
      console.log(this.file.type);
      this.$store.state.file_uploaded = this.file;
      this.type = this.file.type;
    }
  },
  watch: {
    $v: {
      handler: function(val) {
        if (!val.$invalid) {
          this.$emit("can-continue", { value: true });
        } else {
          this.$emit("can-continue", { value: false });
        }
      },
      deep: true
    },
    clickedNext(val) {
      if (val === true) {
        console.log("next", val);
        this.$v.form.$touch();
      }
    }
  },

  mounted() {
    if (this.continue) {
      this.$emit("can-continue", { value: true });
    } else {
      this.$emit("can-continue", { value: false });
    }
  }
};
</script>