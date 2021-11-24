import Vue from 'vue'
import Router from 'vue-router'
import Movies from '@/views/Movies.vue'
import MovieDetail from '@/views/MovieDetail.vue'
import Login from '@/views/Login.vue'
import Mypage from '@/views/Mypage.vue'
import Recruit from '@/views/Recruit.vue'
import RecruitForm from '@/components/RecruitForm.vue'
import RecruitArticleDetail from '@/components/RecruitArticleDetail.vue'
import Tournament from '@/views/Tournament.vue'

Vue.use(Router)

export const constantRoutes = [
  {
    path: '/movies',
    name: 'Movies',
    component: Movies,
    meta: {
      title: "MVTI"
    },
  },
  {
    path: '/movies/:movie_pk',
    name: 'MovieDetail',
    component: MovieDetail,
    meta: {
      title: "Movie Detail"
    },
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
    props: true,
    meta: {
      title: "Login"
    },
  },
  
  {
    path:'/mypage/:username',
    name:'Mypage',
    component: Mypage,
    meta: {
      title: "My Page"
    },
  },
  {
    path: '/recruits',
    name: 'Recruit',
    component: Recruit,
    meta: {
      title: "OTT 모집 게시판"
    },
  },
  {
    path: '/recruits/create',
    name: 'RecruitForm',
    component: RecruitForm,
    meta: {
      title: "OTT 모집 게시글 작성"
    },
  },
  {
    path: '/recruits/:recruitId',
    name: 'RecruitArticleDetail',
    component: RecruitArticleDetail,
    meta: {
      title: "OTT 모집 게시글"
    },
  },
  {
    path: '/tournament',
    name: 'Tournament',
    component: Tournament,
    meta: {
      title: "이상형 월드컵"
    },
  },
]

const createRouter = () => new Router({
  mode: 'history',
  scrollBehavior: () => ({ y: 0 }),
  base: process.env.BASE_URL,
  routes: constantRoutes
})

const router = createRouter()

router.afterEach((to) => {
  const title = to.meta.title === undefined ? 'MVTI' : to.meta.title;
  Vue.nextTick(() => {
    document.title = title;
  });
});

export default router

