import Vue from "vue";
import Vuex from "vuex";
import Axios from "axios";
import jwt_decode from "jwt-decode";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    accessToken: localStorage.getItem("t"),
    refreshToken: null,
    user: {
      first_name: "",
      last_name: "",
      email: "",
    },
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
  getters: {
    loggedIn(state) {
      return state.accessToken != null;
    },
  },
  mutations: {
    updateStorage(state, { accessToken, first_name, last_name, email }) {
      localStorage.setItem("t", accessToken);

      state.accessToken = accessToken;
      state.user.first_name = first_name;
      state.user.last_name = last_name;
      state.user.email = email;
    },
    removeToken(state) {
      localStorage.removeItem("t");
      state.accessToken = null;
    },
  },
  actions: {
    userLogin(context, userData) {
      console.log(userData);
      return new Promise((resolve) => {
        Axios.post("http://localhost:8000/api/token/", {
          email: userData.email,
          password: userData.password,
        }).then((response) => {
          console.log(response.data);
          context.commit("updateStorage", {
            accessToken: response.data.token,
            first_name: response.data.first_name,
            last_name: response.data.last_name,
            email: response.data.email,
          });
          resolve();
        });
      });
    },
    userLogout(context) {
      return new Promise((resolve) => {
        context.commit("removeToken");
        resolve();
      });
    },
    // refreshToken(context, userData) {
    //   return new Promise((resolve) =>
    //     Axios.post("http://localhost:8000/api/token/refresh/", {
    //       token: this.state.accessToken,
    //     }).then((response) => {
    //       console.log(response.data);
    //       context.commit("updateStorage", {
    //         accessToken: response.data.token,
    //         first_name: response.data.first_name,
    //         last_name: response.data.last_name,
    //         email: response.data.email,
    //       });
    //       resolve();
    //     });
    //     )
    //   );
    // },
    userRegister(context, userData) {
      return new Promise((resolve) => {
        Axios.post("http://localhost:8000/register/", {
          email: userData.email,
          password: userData.password,
          first_name: userData.first_name,
          last_name: userData.last_name,
        }).then((response) => {
          console.log(response.data);
          context.commit("updateStorage", {
            accessToken: response.data.token,
            first_name: response.data.first_name,
            last_name: response.data.last_name,
            email: response.data.email,
          });
          resolve();
        });
      });
    },
    inspectToken() {
      const token = this.state.accessToken;
      if (token) {
        const decoded = jwt_decode(token);
        const exp = decoded.exp;
        const orig_iat = decoded.orig_iat;
        console.log(decoded);
        if (
          exp - Date.now() / 1000 < 1800 &&
          Date.now() / 1000 - orig_iat < 628200
        ) {
          this.dispatch("userLogin", {
            email: this.state.user.email,
            password: this.state.user.password,
          }).then(() => {
            this.$router.push({ name: "home" });
          });
        } else if (exp - Date.now() / 1000 < 1800) {
          this.$router.push({ name: "login" });
        } else {
          this.$router.push({ name: "login" });
        }
      }
    },
  },
});
