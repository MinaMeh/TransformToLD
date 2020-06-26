import Vue from "vue";
import Vuex from "vuex";
import Axios from "axios";
//import jwt_decode from "jwt-decode";

Vue.use(Vuex);

export default new Vuex.Store({

    state: {
        jwt: localStorage.getItem("t"),
        user: {
            first_name: localStorage.getItem("first_name"),
            last_name: localStorage.getItem("last_name"),
            email: localStorage.getItem("email"),
        },
        properties: [],
        vocabs: [],
        file_type: null,
        file_uploaded: "",
        file_content: [],
        filename: "",
        progress: true,
        project_id: "",
        project_name: "",
        description: "",
        licence: "",
        //projects: [],
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
            return state.jwt != null;
        },
    },
    mutations: {
        updateStorage(state, { newToken, first_name, last_name, email }) {
            localStorage.setItem("t", newToken);
            state.jwt = newToken;
            state.user.first_name = first_name;
            state.user.last_name = last_name;
            state.user.email = email;
            localStorage.getItem("first_name", first_name);
            localStorage.getItem("last_name", last_name);
            localStorage.getItem("email", email);
        },
        removeToken(state) {
            localStorage.removeItem("t");
            state.jwt = null;
        },
    },
    actions: {
        userLogin(context, userData) {
            console.log(userData);
            return new Promise((resolve, reject) => {
                Axios.post("http://localhost:8000/api/token/", {
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

        /*        refreshToken(context) {
        //console.log(userData);
        const payload = {
            token: this.state.jwt
        }
        return new Promise((resolve, reject) => {
            Axios.post("http://localhost:8000/api/token/refresh/",
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
                Axios.post("http://localhost:8000/register/", {
                    email: userData.email,
                    password: userData.password,
                    first_name: userData.first_name,
                    last_name: userData.last_name,
                }).then((response) => {
                    console.log(response.data);
                    context.commit("updateStorage", {
                        jwt: response.data.token,
                        first_name: response.data.first_name,
                        last_name: response.data.last_name,
                        email: response.data.email,
                    });
                    resolve();
                });
            });
        },
        /*inspectToken() {
                    const token = this.state.jwt;
                    if (token) {
                        const decodedData = jwt_decode(token);
                        const expirationDate = decodedData.exp;
                        const orig_iat = decodedData.orig_iat;
                        console.log(decodedData);
                        if (
                            expirationDate - (Date.now() / 1000) < 1800 &&
                            (Date.now() / 1000) - orig_iat < 628200) {
                            this.dispatch("userLogin", {
                                email: this.state.user.email,
                                password: this.state.user.password,
                            }).then(() => {
                                this.$router.push({
                                    name: "home"
                                });
                            });
                        } else if (expirationDate - (Date.now() / 1000) < 1800) {
                            this.$router.push({
                                name: "login"
                            });
                        } else {
                            this.$router.push({
                                name: "login"
                            });
                        }
                    }
                },
                */
    },
});