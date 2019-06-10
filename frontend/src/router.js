import Vue from 'vue'
import Router from 'vue-router'
import Store from './store'

Vue.use(Router)

let router = new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'payments',
      component: () => import(/* webpackChunkName: "payments" */ './components/PaymentsContainer.vue'),
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/login',
      name: 'login',
      component: () => import(/* webpackChunkName: "login" */ './components/LoginContainer.vue'),
    },
    {
      path: '/logout',
      name: 'logout',
      component: () => import(/* webpackChunkName: "logout" */ './components/Logout.vue'),
      meta: {
        requiresAuth: true
      }
    },
  ]
})

router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (Store.getters.isLoggedIn) {
      next()
      return
    }
    next('/login')
  } else {
    if (to.name === 'login' && Store.getters.isLoggedIn) {
      next('/')
      return
    }
    next()
  }
})

export default router
