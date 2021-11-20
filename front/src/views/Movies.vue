<template>
  <div class="main">
    <MoviesSlider :movies="highscore_movies"/>
    <div class="section">
      <div class="section-header">곧 개봉할 영화</div>
      <MovieCarousel :movies="latest_movies"/>
    </div>
    <div class="section">
      <div class="section-header">많은 사람이 본 영화</div>
      <MovieCarousel :movies="like_movies"/>
    </div>

  </div>
</template>

<script>
import MoviesSlider from '@/components/MoviesSlider.vue'
import MovieCarousel from '@/components/MovieCarousel.vue'
import axios from 'axios'

const BACKEND = process.env.VUE_APP_BACKEND_LINK
export default {
  name : 'Movies',
  components : {
    MoviesSlider,
    MovieCarousel,
  },
  data : function(){
    return {
      latest_movies : [],
      highscore_movies : [],
      like_movies : [],
    }
  },
  methods : {
    getLatestMovies : function(){
      const link = 'movies'
      axios.get(BACKEND+link)
        .then(res =>{
          this.latest_movies = res.data.latest_movies
          this.highscore_movies = res.data.highscore_movies
          this.like_movies = res.data.like_movies
        })
    }
  },
  created : function(){
    this.getLatestMovies()
  }
}
</script>

<style scoped>

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