import Vue from "vue";
import App from "./App.vue";
import TextHighlight from "vue-text-highlight";
import "./../node_modules/bulma/css/bulma.css";
import store from "./store";
import "@fortawesome/fontawesome-free/css/all.css";
import "@fortawesome/fontawesome-free/js/all.js";
import vuetify from "./plugins/vuetify";

import router from "./routes";

import moment from 'moment';

Vue.filter('formatDate', function(value) {
    if (value) {
        return moment(String(value)).format('MMMM Do YYYY, h:mm:ss a')
    }
});

Vue.config.productionTip = false;
Vue.component("text-highlight", TextHighlight);
/*
store
    .dispatch("inspectToken")
    .then(() => {
        console.log(store.accessToken);
    })
    .catch((err) => {
        console.log(err);
    });
*/
new Vue({
    router,
    store,
    vuetify,
    render: (h) => h(App),
}).$mount("#app");