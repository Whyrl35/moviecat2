import Vue from 'vue'
import VueRouter from 'vue-router'
import store from '../store.js'
import Home from '../views/Home.vue'
import Movie from '../views/Movie.vue'
import Search from '../views/Search.vue'
import Login from '../views/Login.vue'
import Add from '../views/Add.vue'
import AddMovie from '../views/AddMovie.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'home',
    component: Home
  },
  {
    path: '/movie',
    name: 'movie',
    component: Movie
    //meta: {
    //  requiresAuth: true
    //}
  },
  {
    path: '/login',
    name: 'login',
    component: Login
  },
  {
    path: '/search/:string',
    name: 'search',
    component: Search
  },
  {
    path: '/add',
    name: 'add',
    component: Add,
    meta: {
      requiresAuth: true
    }
  },
  {
    path: '/add/:type/:id',
    name: 'add_movie',
    component: AddMovie,
    meta: {
      requiresAuth: true
    }
  },

]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

router.beforeEach((to, from, next) => {
  if(to.matched.some(record => record.meta.requiresAuth)) {
    if (store.getters.isLoggedIn) {
      next()
      return
    }
    next('/login')
  } else {
    next()
  }
})

export default router
