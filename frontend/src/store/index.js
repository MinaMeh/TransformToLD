import Vue from "vue";
import Vuex from "vuex";
import instance from "@/services/MainService";
import routes from "@/router";
import jwt_decode from "jwt-decode";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    jwt: localStorage.getItem("t"),
    user_id: localStorage.getItem("user_id"),
    user: {
      first_name: localStorage.getItem("first_name"),
      last_name: localStorage.getItem("last_name"),
      email: localStorage.getItem("email"),
    },
    metadata: {
      creator:
        localStorage.getItem("first_name") +
        " " +
        localStorage.getItem("last_name"),
      license: "",
      description: "",
      title: "",
      subject: "",
    },
    vocabs: [],
    file_type: null,
    file_uploaded: "",
    file_content: [],
    filename: "",
    progress: false,
    project_id: "",
    project_name: "",
    description: "",
    licence: "",
    guide: true,
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
      rowClass: "",
      headersId: [],
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
      return state.jwt != null;
    },
  },
  mutations: {
    updateStorage(state, { jwt, first_name, last_name, email, user_id }) {
      localStorage.setItem("t", jwt);
      state.jwt = jwt;
      state.user.first_name = first_name;
      state.user.last_name = last_name;
      state.user.email = email;
      state.user_id = user_id;
      state.creator = first_name + " " + last_name;
      localStorage.setItem("first_name", first_name);
      localStorage.setItem("last_name", last_name);
      localStorage.setItem("email", email);
      localStorage.setItem("user_id", user_id);
    },
    removeToken(state) {
      localStorage.removeItem("t");
      localStorage.removeItem("first_name");
      localStorage.removeItem("last_name");
      localStorage.removeItem("email");
      localStorage.removeItem("user_id");

      state.jwt = null;
    },
  },
  actions: {
    userLogin(context, userData) {
      console.log(userData);
      return new Promise((resolve, reject) => {
        instance
          .post("/api/token/", {
            email: userData.email,
            password: userData.password,
          })
          .then((response) => {
            console.log(response.data);
            context.commit("updateStorage", {
              jwt: response.data.token,
              first_name: response.data.first_name,
              last_name: response.data.last_name,
              email: response.data.email,
              user_id: response.data.user_id,
            });
            resolve();
          })
          .catch((err) => {
            reject(err);
          });
      });
    },
    userLogout(context) {
      if (context.getters.loggedIn) {
        return new Promise((resolve) => {
          localStorage.removeItem("t");
          context.commit("removeToken");
          resolve();
        });
      }
    },
    /*
    refreshToken(context, userData) {
      return new Promise((resolve) =>
        instance.post("api/token/refresh/", {
          token: this.state.accessToken,
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
        )
      );
    },*/
    refreshToken(context, token) {
      return new Promise((resolve) => {
        instance
          .post("api/token/refresh/", {
            token: token,
          })
          .then((response) => {
            console.log("refresh token", response.data);
            context.commit("updateStorage", {
              jwt: response.data.token,
              first_name: response.data.first_name,
              last_name: response.data.last_name,
              email: response.data.email,
            });
            resolve();
          })
          .catch((error) => {
            console.log(error);
          });
      });
    },
    /*        refreshToken(context) {
        //console.log(userData);
        const payload = {
            token: this.state.jwt
        }
        return new Promise((resolve, reject) => {
            instance.post("api/token/refresh/",
                payload
            ).then((response) => {
                console.log(response.data);
                context.commit("updateStorage", response.data.token);
                resolve();
            }).catch(err => {
                reject(err);
            })
        });
    },
*/

    userRegister(context, userData) {
      return new Promise((resolve) => {
        instance
          .post("register/", {
            email: userData.email,
            password: userData.password,
            first_name: userData.first_name,
            last_name: userData.last_name,
          })
          .then((response) => {
            console.log(response.data);
            context.commit("updateStorage", {
              jwt: response.data.token,
              first_name: response.data.first_name,
              last_name: response.data.last_name,
              email: response.data.email,
              user_id: response.data.id,
            });
            resolve();
          });
      });
    },
    inspectToken() {
      const token = this.state.jwt;
      if (token) {
        const decodedData = jwt_decode(token);
        const expirationDate = decodedData.exp;
        console.log("state jwt ", this.state.jwt);
        console.log("decoded data ", decodedData);
        if (expirationDate * 1000 < Date.now()) {
          routes.push({
            name: "login",
          });
        }
      }
    },
  },
});
