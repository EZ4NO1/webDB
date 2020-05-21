import Vue from 'vue'
import VueRouter from 'vue-router'
import App from '../pages/login/App.vue'




const routerPush = VueRouter.prototype.push
VueRouter.prototype.push = function push(location) {
  return routerPush.call(this, location).catch(error => error)
}
Vue.use(VueRouter)

  const routes = [
  {
    path: '/',
    component: App
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
