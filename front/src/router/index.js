import Vue from 'vue'
import VueRouter from 'vue-router'
import Movies from '@/views/Movies.vue'
import MovieDetail from '@/views/MovieDetail.vue'
import Login from '@/views/Login.vue'
import Mypage from '@/views/Mypage.vue'

import OTTCommunity from '@/views/OTTCommunity.vue'
import OTTArticle from '@/views/OTTArticle.vue'
import MovieCommunity from '@/views/MovieCommunity.vue'
import MovieArticle from '@/views/MovieArticle.vue'

import Tournament from '@/views/Tournament.vue'
import PageNotFound from '@/views/PageNotFound.vue'
Vue.use(VueRouter)

const routes = [
  {
    path: '/movies',
    name: 'Movies',
    component: Movies
  },
  {
    path: '/movies/:movie_pk',
    name: 'MovieDetail',
    component: MovieDetail
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
    props: true
  },
  
  {
    path:'/mypage/:username',
    name:'Mypage',
    component: Mypage,
  },
  {
    path: '/OTTcommunity',
    name: 'OTTCommunity',
    component: OTTCommunity
  },
  {
    path: '/OTTcommunity/:detail',
    name: 'OTTArticle',
    component: OTTArticle
  },
  {
    path: '/Moviecommunity',
    name: 'MovieCommunity',
    component: MovieCommunity
  },
  {
    path: '/Moviecommunity/:detail',
    name: 'MovieArticle',
    component: MovieArticle
  },

  {
    path: '/tournament',
    name: 'Tournament',
    component: Tournament
  },
  {
    path: '/404',
    name: '404Page',
    component: PageNotFound
  },
  {
    path : '*',
    redirect : '/404'
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})
router.afterEach(() => {
  window.scrollTo(0,0);
})
export default router

