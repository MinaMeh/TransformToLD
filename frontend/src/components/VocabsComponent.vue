<template>
  <v-container>
    <v-row no-gutters class="mt-12">
      <v-col cols="12">
        <v-progress-linear
          v-if="$store.state.progress"
          class="mt-10"
          indeterminate
          color="light-blue"
          height="10"
          value="10"
          striped
        ></v-progress-linear>

        <h1>Vocabularies</h1>
        <v-row>
          <v-col cols="2" class="mt-3" align="left" justify="left">
            <v-btn @click="addAllVocabs()" color="success">Add All</v-btn>
          </v-col>
          <v-col cols="2" class="mt-3" align="left" justify="left">
            <v-btn @click="deleteAllVocabs()" color="error">Delete All</v-btn>
          </v-col>
        </v-row>
        <v-card flat>
          <v-chip
            color="primary"
            class="ma-1"
            v-for="(vocab,index) in selectedVocabs"
            :key="index"
            close
            @click:close="deleteVocab(vocab)"
          >{{vocab.prefix}}</v-chip>
        </v-card>
      </v-col>
    </v-row>
    <v-row no-gutters>
      <v-col cols="12">
        <v-card flat>
          <v-card-title>
            <v-row>
              <v-col cols="12">
                <v-text-field
                  v-model="search"
                  prepend-icon="mdi-magnify"
                  label="Search"
                  single-line
                  hide-details
                  class="mb-5 vocabs"
                ></v-text-field>
              </v-col>
            </v-row>
          </v-card-title>
          <v-data-table :headers="headers" :items="vocabs" :search="search">
            <template v-slot:item="row">
              <tr>
                <td>{{row.item.prefix}}</td>
                <td>{{row.item.title}}</td>
                <td>
                  <a v-bind:href="row.item.uri" target="__">{{row.item.uri}}</a>
                </td>
                <td>
                  <v-btn class="mx-2" fab dark small color="green" @click="addVocab(row.item)">
                    <v-icon dark>mdi-plus</v-icon>
                  </v-btn>
                </td>
              </tr>
            </template>
          </v-data-table>
          <v-progress-linear
            v-if="loading"
            class="mt-10"
            indeterminate
            color="light-blue"
            height="10"
            value="10"
            striped
          ></v-progress-linear>

          <v-sheet v-if="loading" color="grey lighten-4" class="px-3 pt-3 pb-3">
            <v-skeleton-loader class="mx-auto" type="table-tbody"></v-skeleton-loader>
          </v-sheet>
        </v-card>
      </v-col>
    </v-row>
    <v-tour name="myTour" :steps="steps"></v-tour>
  </v-container>
</template>
<script>
import { validationMixin } from "vuelidate";
import instance from "@/services/MainService";

export default {
  props: ["clickedNext", "currentStep"],
  mixins: [validationMixin],
  data() {
    return {
      continue: true,
      search: "",
      loading: true,
      headers: [
        { text: "Prefix", value: "prefix" },
        { text: "Title", value: "title" },
        { text: "URI", value: "uri" },
        { text: "", value: "", align: "center" },
      ],
      vocabs: [],
      selectedVocabs: [],
      steps: [
        {
          target: ".vocabs", // We're using document.querySelector() under the hood
          header: {
            title: "Add Vocabularies",
          },
          content: `Add the vocabularies that you want to use in the mapping`,
          params: {
            enableScrolling: false,
          },
        },
      ],
    };
  },
  computed: {
    filtered_list() {
      return this.vocabs.filter((vocab) => {
        return vocab.prefix.toLowerCase().includes(this.search.toLowerCase());
      });
    },
    guide() {
      return this.$store.state.guide;
    },
  },
  methods: {
    addVocab: function (vocab) {
      var exist = false;
      for (var voc in this.selectedVocabs) {
        if (this.selectedVocabs[voc].prefix == vocab.prefix) {
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
        this.addVocab(this.vocabs[voc]);
      }
    },
    deleteAllVocabs() {
      this.selectedVocabs = [];
      this.$store.state.vocabs = [];
    },

    deleteVocab: function (vocab) {
      this.selectedVocabs.splice(vocab, 1);
      this.$store.state.vocabs.splice(vocab, 1);
    },
  },
  watch: {
    guide(newValue) {
      if (newValue == true) this.$tours["myTour"].start();
      else this.$tours["myTour"].stop();
    },

    $v: {
      handler: function (val) {
        if (!val.$invalid) {
          this.$emit("can-continue", { value: true });
        } else {
          this.$emit("can-continue", { value: false });
        }
      },
      deep: true,
    },
    clickedNext(val) {
      if (val === true) {
        console.log(this.file);

        this.$store.state.vocabs = this.selectedVocabs;

        this.$v.form.$touch();
      }
    },
  },

  mounted() {
    if (this.$store.state.guide) this.$tours["myTour"].start();

    this.$store.state.vocabs = [];
    instance
      .get("vocabs/", {
        headers: {
          "Content-Type": "multipart/form-data",
          Authorization: `JWT ${this.$store.state.jwt}`,
        },
      })
      .then((response) => {
        this.vocabs = response.data;
        console.log(this.vocabs.length);
        this.loading = false;
      })
      .catch((error) => console.log(error));

    if (this.continue) {
      this.$emit("can-continue", { value: true });
    } else {
      this.$emit("can-continue", { value: false });
    }
  },
};
</script>
