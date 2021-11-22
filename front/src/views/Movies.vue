<template>
  <div class="main">
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
      <div class="container-fluid">
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav">
            <a @click="switchSlidMovie(netflix_movies)" class="nav-link button-slider-active button-slider" data-menu="1">Netflix</a>
            <a @click="switchSlidMovie(disney_movies)" class="nav-link button-slider" data-menu="2">Disney +</a>
            <a @click="switchSlidMovie(hulu_movies)" class="nav-link button-slider" data-menu="3">hulu</a>
            <a @click="switchSlidMovie(mvti_movies)" class="nav-link button-slider" data-menu="4">내 MVTI 추천영화</a>
          </ul>
        </div>
      </div>
    </nav>
    <MoviesSlider :movies="selected_movies"/>

    <div class="section">
      <div class="section-header">인기 영화</div>
      <MovieCarousel :movies="popular_movies"/>
    </div>
    <div class="section">
      <div class="section-header">{{ first_genre }}</div>
      <MovieCarousel :movies="first_genre_movies"/>
    </div>
    <div class="section">
      <div class="section-header">{{ secound_genre }}</div>
      <MovieCarousel :movies="secound_genre_movies"/>
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
      selected_movies: [],
      netflix_movies : [],
      disney_movies: [],
      hulu_movies: [],
      // mvti_movies: [],
      popular_movies: [],
      // first_genre: '',
      // first_genre_movies: [],
      // secound_genre: '',
      // secound_genre_movies: [],
    }
  },
  methods : {
    getMovies : function() {
      const link = 'movies'
      axios.get(BACKEND+link)
        .then(res =>{
          console.log(res.data)
          this.selected_movies = res.data.netflix_movies
          this.netflix_movies = res.data.netflix_movies
          this.disney_movies = res.data.disney_movies
          this.hulu_movies = res.data.hulu_movies
          // this.mvti_movies = res.data.mvti_movies
          this.popular_movies = res.data.popular_movies
          // this.first_genre = res.data.first_genre
          // this.first_genre_movies = res.data.first_genre_movies
          // this.secound_genre = res.data.secound_genre
          // this.secound_genre_movies = res.data.secound_genre_movies
        })
        .catch(error=> {
          alert(error)
          console.log(BACKEND+link)
        })
    },
    switchSlidMovie: function(select_movie) {
      this.selected_movies = select_movie
    }

  },
  created : function(){
    this.getMovies()
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