
import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import axios from 'axios'
import moment from 'moment'
import { Promised } from 'vue-promised'

Vue.config.productionTip = false
Vue.prototype.$http = axios;
const token = localStorage.getItem('token')
if (token) {
  Vue.prototype.$http.defaults.headers.common['Authorization'] = 'Token ' + token
}

Vue.component('Promised', Promised)

Vue.filter('formatDate', function(value) {
  if (value) {
    return moment(String(value)).format('DD/MM/YYYY hh:mm:ss')
  }
})

new Vue({
  router,
  store,
  axios,
  render: h => h(App)
}).$mount('#app')
