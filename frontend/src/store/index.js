import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    properties: [],
    vocabs: [],
    file_uploaded: "",
    file_content: [],
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
