import axios from 'axios'

const Api = () =>
  axios.create({
    baseURL: process.env.VUE_APP_API_URL + '/api/',
    data: {},
  })

export default {
  get: (url, config) =>
    Api().get(`${url}`, config)
      .then(response => Promise.resolve(response.data))
      .catch(error => Promise.reject(error)),
  post: (url, data, config) =>
    Api().post(`${url}`, data, config)
      .then(response => Promise.resolve(response))
      .catch(error => Promise.reject(error)),
}
