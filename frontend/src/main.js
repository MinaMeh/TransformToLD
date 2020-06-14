import Vue from "vue";

import App from "./App.vue";

import TextHighlight from "vue-text-highlight";
import "@fortawesome/fontawesome-free/css/all.css";
import "@fortawesome/fontawesome-free/js/all.js";
import vuetify from "./plugins/vuetify";

import store from "./store/index.js";
import router from './router'
import GSignInButton from 'vue-google-signin-button'

Vue.use(GSignInButton);

Vue.config.productionTip = false;
Vue.component("text-highlight", TextHighlight);

new Vue({
    store,
    vuetify,
    router,
    render: h => h(App)
}).$mount("#app");