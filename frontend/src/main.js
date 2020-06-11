import Vue from "vue";
import VueRouter from 'vue-router';

import App from "./App.vue";

import TextHighlight from "vue-text-highlight";
import "@fortawesome/fontawesome-free/css/all.css";
import "@fortawesome/fontawesome-free/js/all.js";
import vuetify from "./plugins/vuetify";

import store from "./store";

import VueAuthenticate from 'vue-authenticate'
import VueAxios from 'vue-axios'
import axios from 'axios';
import {
    routes
} from './routes';

Vue.use(VueRouter);
Vue.use(VueAxios, axios)
Vue.use(VueAuthenticate, {
    providers: {
        google: {
            clientId: '265982645018-0qvdbb07ltu6uou8j4pbdelk76l1evef.apps.googleusercontent.com',
            redirectUri: 'http://localhost:8080/',
            url: 'http://localhost:8000/api/login/social/token_user/google/',
        }
    }
});
const router = new VueRouter({
    mode: 'history',
    routes,
});


Vue.config.productionTip = false;
Vue.component("text-highlight", TextHighlight);

new Vue({
    store,
    vuetify,
    router,
    render: h => h(App)
}).$mount("#app");