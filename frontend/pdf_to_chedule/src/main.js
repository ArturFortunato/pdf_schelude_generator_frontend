import Vue from 'vue'
import App from './App.vue'
import vuetify from './plugins/vuetify';
import "vuetify/dist/vuetify.min.css";
import VueRouter from 'vue-router'

import Schedules from './components/Schedules'
import Search from './components/Search'

Vue.config.productionTip = false

Vue.use(VueRouter)

const routes = [
  { 
    path: '/',
    component: Search
  },
  { 
    path: '/schedules/:courses',
    component: Schedules,
    props: {
      default: true
    }
  }
]

const router = new VueRouter({
  routes 
})

new Vue({
  vuetify,

  icons: {
    iconfont: 'md', // 'mdi' || 'mdiSvg' || 'md' || 'fa' || 'fa4' || 'faSvg'
  },

  router,
  render: h => h(App)
}).$mount('#app')
