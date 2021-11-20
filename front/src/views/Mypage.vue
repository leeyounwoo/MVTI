<template>
  <div class="main" style="padding-top:55px;">
    <userInformation/>
    <div class="section">
      <div class="section-header">영화월드컵 우승작</div>
      <MovieCarousel :movies="win_movies"/>
    </div>
    <div class="section">
      <div class="section-header">좋아한 작품</div>
      <MovieCarousel :movies="like_movies"/>
    </div>
  </div>
</template>
<script>
import userInformation from '@/components/userInformation'
import MovieCarousel from '@/components/MovieCarousel.vue'
import movieMixin from "@/mixins/movieMixin"
import axios from 'axios'

const BACKEND = process.env.VUE_APP_BACKEND_LINK


export default {
  name:'Mypage',
  components:{
    userInformation,
    MovieCarousel,
  },
  mixins : [movieMixin],
  data : function(){
    return {
      win_movies : [],
      like_movies : [],
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
          this.like_movies = res.data.likeMovies
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