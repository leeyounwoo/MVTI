<template>
  <div class="main" style="padding-top:55px;">
    <userInformation/>
      
    <div>
      <h2 class="else-movieslide">인기 영화</h2><hr>
      <carousel-3d :disable3d="true" :space="230" :clickable="false" :controls-visible="true" :width="200" :height="270" :autoplay="true" :autoplay-timeout="3000">
        <slide v-for="(slide_2d, i) in slides_2d" :key="i" :index="i">
          <img 
            :src="`https://image.tmdb.org/t/p/original${win_movies[i].poster_path}`" alt="poster" style="width:100%; height:100%; cursor: pointer;" class="">
        </slide>
      </carousel-3d>
    </div>
    
  </div>
</template>
<script>
import userInformation from '@/components/userInformation'
import movieMixin from "@/mixins/movieMixin"
import axios from 'axios'

import Vue from 'vue'
import { Carousel3d, Slide } from 'vue-carousel-3d';
Vue.use('Carousel3d')

const BACKEND = process.env.VUE_APP_BACKEND_LINK


export default {
  name:'Mypage',
  components:{
    userInformation,
    Carousel3d,
    Slide,
  },
  mixins : [movieMixin],
  data : function(){
    return {
      win_movies : [],
      slides: 0,
      slides_2d: 0,
      
    }
  },
  methods : {
    getMovies : function(){
      axios({
        method: 'get',
        url: `${BACKEND}movies/mypageMovie/${this.$route.params.username}`,
      })
        .then(res => {
          console.log(res)
          this.win_movies = res.data.winMovies
          this.slides = this.win_movies.length
          this.slides_2d = this.win_movies.length
          console.log(this.win_movies)
        })
        .catch(() =>{
          console.log(this.$route.params.username)
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