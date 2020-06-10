import Vue from "vue";
import App from "./App.vue";
import TextHighlight from "vue-text-highlight";
import "./../node_modules/bulma/css/bulma.css";
import store from "./store";
import "@fortawesome/fontawesome-free/css/all.css";
import "@fortawesome/fontawesome-free/js/all.js";
import vuetify from "./plugins/vuetify";
import router from './router'

Vue.config.productionTip = false;
Vue.component("text-highlight", TextHighlight);

new Vue({
  router,
  store,
  vuetify,
  render: h => h(App)
}).$mount("#app");
