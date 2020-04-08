import Vue from 'vue'
import App from './App.vue'
import './../node_modules/bulma/css/bulma.css'
import store from './store'
import '@fortawesome/fontawesome-free/css/all.css'
import '@fortawesome/fontawesome-free/js/all.js'
import vuetify from './plugins/vuetify';

Vue.config.productionTip = false

new Vue({
  store,
  vuetify,
  render: h => h(App)
}).$mount('#app')
