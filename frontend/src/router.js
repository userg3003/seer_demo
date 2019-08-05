import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      methods: {
        predict () {
          // eslint-disable-next-line no-undef
          return axios.post('/api/blocks/save', this.items)
        }
      }
    }
  ]
})
