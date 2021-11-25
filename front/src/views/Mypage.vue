<template>
  <div class="main" style="padding-top:55px;">
    <!-- <userInformation/> -->
      
    <div>
      <h2 style="text-align: center; color: #B00084;">이상형 월드컵 우승작</h2><hr>
      <carousel-3d :disable3d="true" :space="230" :display="5" :clickable="false" :controls-visible="true" :width="200" :height="270" :autoplay="true" :autoplay-timeout="3000">
        <slide v-for="(slide_2d, i) in slides_2d" :key="i" :index="i">
          <img 
            :src="`https://image.tmdb.org/t/p/original${win_movies[i].poster_path}`" alt="poster" style="width:100%; height:100%; cursor: pointer;" class="">
        </slide>
      </carousel-3d>
      <h3>{{ first_name }}</h3>
      <img :src="`${first_img}`" alt="poster" style="width:30%; height:30%;" class="">
      <h3>{{ second_name }}</h3>
      <img :src="`${second_img}`" alt="poster" style="width:30%; height:30%;" class="">
      <h3>{{ third_name }}</h3>
      <img :src="`${third_img}`" alt="poster" style="width:30%; height:30%;" class="">
    </div>
    <h2 style="color: #fff;">구매한 OTT 서비스 계정</h2>
    <div class="d-flex">

      <ul v-for="recruit in recruits" :key="recruit.id">
        <span class="m-2">
          <!-- <p class="indent" style="font-size:17px">&ensp;<strong>{{review.user}}</strong></p> -->
          <p><strong>OTT: {{recruit.ott_name}}</strong></p>
          <p>ID: {{recruit.public_id}}</p>
          <p>PW: {{recruit.public_pw}}</p>

        </span>
      </ul>
    </div>
    <div style="color: #fff;">마일리지: {{userInformation.money}}원</div>
  </div>
</template>
<script>
// import userInformation from '@/components/userInformation'
import movieMixin from "@/mixins/movieMixin"
import axios from 'axios'

import Vue from 'vue'
import { Carousel3d, Slide } from 'vue-carousel-3d';
Vue.use('Carousel3d')

const BACKEND = process.env.VUE_APP_BACKEND_LINK


export default {
  name:'Mypage',
  components:{
    // userInformation,
    Carousel3d,
    Slide,
  },
  mixins : [movieMixin],
  data : function(){
    return {
      win_movies : [],
      slides_2d: 0,
      count: 0,
      recruits: [],
      userInformation: '',
      first_name : '',
      first_img : '',
      second_name : '',
      second_img : '',
      third_name : '',
      third_img : '',
    }
  },
  methods : {
    getMovies : function(){
      axios({
        method: 'get',
        url: `${BACKEND}movies/mypageMovie/${this.$route.params.username}`,
      })
        .then(res => {
          this.win_movies = res.data.winMovies
          this.slides_2d = this.win_movies.length
          this.first_name = res.data.first_name
          this.first_img = res.data.first_img
          this.second_name = res.data.second_name
          this.second_img = res.data.second_img
          this.third_name = res.data.third_name
          this.third_img = res.data.third_img
          console.log(this.win_movies)
        })
        .catch(() =>{
          // console.log(this.$route.params.username)
          alert("없는 회원 정보입니다.")
          this.$router.push({name : 'Movies'})
        })
    },
    getRecruits: function() {
      console.log('OTT')
      axios({
        method: 'get',
        url: `${BACKEND}recruits/mypageRecruit/${this.$route.params.username}`,
      })
        .then(res => {
          this.recruits = res.data.myRecruits
          // console.log(this.recruits)
        })
        .catch(() =>{
          alert("없는 회원 정보입니다.")
          this.$router.push({name : 'Movies'})
        })
    },
    getUser: function() {
      axios({
        method: 'get',
        url: `${BACKEND}accounts/mypageUser/${this.$route.params.username}`,
      })
        .then(res => {
          this.userInformation = res.data
          console.log(res.data)
        })
        .catch(() =>{
          alert("없는 회원 정보입니다.")
          this.$router.push({name : 'Movies'})
        })
    },
    loginCheck : function(){
      if (!this.$store.state.token){
        const detailItem ={
          name: 'Mypage',
          params: this.$route.params.username
        }
        this.$store.dispatch('setNextPage',detailItem)
        this.$router.push({name : 'Login'})
      }
    }
  },
  created : function(){
    this.loginCheck()
    this.getMovies()
    this.getRecruits()
    this.getUser()
  },
}
</script>

<style>

.main {
  background : #262626;
}

.section {
  margin : 20px;
}
.section-header {
  color : #ffffff;
  margin-bottom: 30px;
  padding-left: 20px;
  text-transform: uppercase;
  font-size: 2rem;
  font-weight: 700;
  border-left: 4px solid #c0392b;
  display: flex;
  align-items: center;
}
</style>