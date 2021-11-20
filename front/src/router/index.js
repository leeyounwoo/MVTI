import Vue from 'vue'
import VueRouter from 'vue-router'
import Intro from '@/views/Intro.vue'
import Movies from '@/views/Movies.vue'
import Login from '@/views/Login.vue'
import Mypage from '@/views/Mypage.vue'
import MovieDetail from '@/views/MovieDetail.vue'
import Community from '@/views/Community.vue'
import Review from '@/views/Review.vue'
import Tournament from '@/views/Tournament.vue'
import PageNotFound from '@/views/PageNotFound.vue'
Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Intro',
    component: Intro
  },
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
    path: '/community',
    name: 'Community',
    component: Community
  },
  {
    path: '/community/:detail',
    name: 'Review',
    component: Review
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

