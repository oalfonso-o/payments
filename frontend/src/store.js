import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'

Vue.use(Vuex);

const state = {
  auth_status: '',
  token: localStorage.getItem('token') || '',
  user : localStorage.getItem('user') || '',
};

const mutations = {
  AUTH_REQUEST(state){
    state.auth_status = 'loading'
  },
  AUTH_SUCCESS(state, token, user){
    state.auth_status = 'success'
    state.token = token
    state.user = user
  },
  AUTH_ERROR(state){
    state.auth_status = 'error'
  },
  LOGOUT(state){
    state.auth_status = ''
    state.token = ''
    state.user = ''
  },
};

const actions = {
  login({commit}, login_data){
    return new Promise((resolve, reject) => {
      commit('AUTH_REQUEST')
      axios({url: process.env.VUE_APP_API_URL + '/api/login', data: login_data, method: 'POST' })
      .then(resp => {
        const token = resp.data.token
        const user = login_data.username
        localStorage.setItem('token', token)
        localStorage.setItem('user', user)
        axios.defaults.headers.common['Authorization'] = 'Token ' + token
        commit('AUTH_SUCCESS', token, user)
        resolve(resp)
      })
      .catch(err => {
        commit('AUTH_ERROR')
        localStorage.removeItem('token')
        reject(err)
      })
    })
  },
  logout({commit}){
    return new Promise((resolve) => {
      commit('LOGOUT')
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      delete axios.defaults.headers.common['Authorization']
      resolve()
    })
  }
};

const getters = {
  isLoggedIn: state => !!state.token,
  authStatus: state => state.status,
};

export default new Vuex.Store({
  state,
  mutations,
  actions,
  getters
});
