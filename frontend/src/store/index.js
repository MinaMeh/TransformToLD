import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    properties: [],
    vocabs: [],
    file_type: null,
    file_uploaded: "",
    file_content: [],
    filename: "",
    progress: true,
    project_name: "",
    text: {
      paragraph: {
        paragraph: "",
        sentences: [],
        terms: [],
        triplets: [],
      },
    },
    csv: {
      separator: ";",
      headers: [],
      lines: 0,
      columns: 0,
      terms: [],
      triplets: [],
    },
    size: 0,
    html: {
      extract_tables: true,
      extract_paragraphs: true,
      tables: [],
      paragraphs: [],
      num_tables: 0,
      num_paragraphs: 0,
      tables_triplets: [],
      paragraphs_triplets: [],
    },
  },
  getters: {},
  mutations: {
    UPDATE_PROPERTIES(state, payload) {
      state.properties = payload.properties;
    },
  },
  actions: {
    addProperties({ commit }, payload) {
      commit("UPDATE_PROPERTIES", payload);
    },
  },
});
