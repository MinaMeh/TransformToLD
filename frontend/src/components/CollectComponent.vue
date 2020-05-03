<template>
  <v-container>
    <v-form>
      <v-row class="mt-10">
        <v-col cols="5">
          <v-text-field
            outlined
            label="Project"
            placeholder="Project Name"
            v-model="form.project_name"
            prepend-icon="mdi-folder"
          ></v-text-field>
        </v-col>
        <v-col cols="1">
          <v-switch v-model="link" label="link"></v-switch>
        </v-col>
        <v-col cols="6" v-if="!link">
          <v-file-input
            outlined
            label="File"
            @change="uploadFile()"
            placeholder="Choose a file"
            v-model="file"
            prepend-icon="mdi-file"
          ></v-file-input>
        </v-col>
        <v-col cols="6" v-if="link">
          <v-text-field outlined label="File Link" placeholder=" File link" prepend-icon="mdi-link"></v-text-field>
        </v-col>
      </v-row>
      <v-row no-gutters>
        <v-col cols="12">
          <h1>Vocabularies</h1>
          <v-card flat>
            <v-chip
              color="primary"
              class="ma-1"
              v-for="(vocab,index) in selectedVocabs"
              :key="index"
            >{{vocab}}</v-chip>
          </v-card>
        </v-col>
      </v-row>
      <v-row no-gutters>
        <v-col cols="12">
          <v-card flat>
            <v-card-title>
              <v-row>
                <v-col cols="10">
                  <v-text-field
                    v-model="search"
                    prepend-icon="mdi-magnify"
                    label="Search"
                    single-line
                    hide-details
                    class="mb-5"
                  ></v-text-field>
                </v-col>

                <v-col cols="2" class="mt-3" align="left" justify="left">
                  <v-btn @click="addAllVocabs()" color="success">Add All</v-btn>
                </v-col>
              </v-row>
            </v-card-title>
            <v-data-table :headers="headers" :items="vocabs" :search="search">
              <template v-slot:item="row">
                <tr>
                  <td>{{row.item.prefix}}</td>
                  <td>{{row.item.title}}</td>
                  <td>{{row.item.uri}}</td>
                  <td>
                    <v-btn
                      class="mx-2"
                      fab
                      dark
                      small
                      color="green"
                      @click="addVocab(row.item.prefix)"
                    >
                      <v-icon dark>mdi-plus</v-icon>
                    </v-btn>
                  </td>
                </tr>
              </template>
            </v-data-table>
            <v-sheet v-if="loading" color="grey lighten-4" class="px-3 pt-3 pb-3">
              <v-skeleton-loader class="mx-auto" type="table-tbody"></v-skeleton-loader>
            </v-sheet>
          </v-card>
        </v-col>
      </v-row>
    </v-form>
  </v-container>
</template>
<script>
import { validationMixin } from "vuelidate";
import axios from "axios";

export default {
  props: ["clickedNext", "currentStep"],
  mixins: [validationMixin],
  data() {
    return {
      form: {
        project_name: "",
        file_link: ""
      },
      loading: true,
      continue: true,
      link: false,
      search: "",
      headers: [
        { text: "Prefix", value: "prefix" },
        { text: "Title", value: "title" },
        { text: "URI", value: "uri" },
        { text: "", value: "", align: "center" }
      ],
      vocabs: [],
      selectedVocabs: [],
      file: null,
      filename: "No file uploaded"
    };
  },
  computed: {
    filtered_list() {
      return this.vocabs.filter(vocab => {
        return vocab.prefix.toLowerCase().includes(this.search.toLowerCase());
      });
    }
  },
  methods: {
    addVocab: function(vocab) {
      var exist = false;
      for (var voc in this.selectedVocabs) {
        if (this.selectedVocabs[voc] == vocab) {
          exist = true;
        }
      }
      if (exist == false) {
        this.selectedVocabs.push(vocab);
        this.$store.state.vocabs.push(vocab);
      }
    },
    addAllVocabs() {
      for (var voc in this.vocabs) {
        this.addVocab(this.vocabs[voc].prefix);
      }
    },
    deleteVocab: function(vocab) {
      this.selectedVocabs.splice(vocab, 1);
    },
    uploadFile() {
      this.$store.state.file_uploaded = this.file;
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
        console.log(this.file);

        this.$store.state.vocabs = this.selectedVocabs;

        this.$v.form.$touch();
      }
    }
  },

  mounted() {
    axios
      .get("http://127.0.0.1:8000/vocabs/")
      .then(response => {
        this.vocabs = response.data;
        console.log(this.vocabs.length);
        this.loading = false;
      })
      .catch(error => console.log(error));

    if (this.continue) {
      this.$emit("can-continue", { value: true });
    } else {
      this.$emit("can-continue", { value: false });
    }
  }
};
</script>
