<template>
  <div class="main">
    <nav class="navbar navbar-expand-lg">
      <div class="container-fluid">
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav" id="ott-button">
            <h2>
              <a @click="switchSlidMovie(netflix_movies)" class="nav-link button-slider-active ott-button" data-menu="1">Netflix</a>
            </h2>
            <h2>
              <a @click="switchSlidMovie(disney_movies)" class="nav-link button-slider ott-button" data-menu="2">Disney +</a>
            </h2>
            <h2>
              <a @click="switchSlidMovie(hulu_movies)" class="nav-link button-slider ott-button" data-menu="3">hulu</a>
            </h2>
            <h2>
              <a @click="switchSlidMovie('mvti_movies')" class="nav-link button-slider ott-button" data-menu="4">내 MVTI 추천영화</a>
            </h2>
          </ul>
        </div>
      </div>
    </nav>

    <div>
      <carousel-3d 
        :autoplay="true"
        :autoplay-timeout="3000" 
        :display="11" 
        :width="400" 
        :height="600" 
      >
        <slide v-for="(slide, i) in slides" :key="i" :index="i">
          <div class="imggroup">
            <img 
              :src="`https://image.tmdb.org/t/p/original${selected_movies[i].poster_path}`"
              style="width:100%; height:100%; cursor: pointer;"
            >
            <star-rating 
              style="position: absolute; top: 0px; text-align: center; size: 50%;}" 
              :rating="parseFloat(popular_movies[i].vote_average) / 2" 
              :read-only="true" 
              :increment="0.01"
            />
            <button class="imggroup-button1" @click="goToMovieDetail(selected_movies[i])">Detail</button>
          </div>
        </slide>
      </carousel-3d>
    </div>

    <br><br><br><br><br>
    <div>
      <h2 class="else-movieslide">인기 영화</h2><hr>
      <carousel-3d :autoplay="true" :autoplay-timeout="3000" :display="7" :disable3d="true" :space="230" :clickable="false" :controls-visible="true" :width="200" :height="270" >
        <slide v-for="(slide_2d, i) in slides_2d" :key="i" :index="i">
          <img 
            :src="`https://image.tmdb.org/t/p/original${popular_movies[i].poster_path}`" 
            style="width:100%; height:100%; cursor: pointer;" 
            class="imggroup"
          >
          <star-rating v-bind:star-size="30" style="position: absolute; top: 0px; text-align: center; size: 50%;}" :rating="parseFloat(popular_movies[i].vote_average) / 2" :read-only="true" :increment="0.01"/>
            <button 
              class="imggroup-button2"
              @click="goToMovieDetail(popular_movies[i])"
            >Detail</button>
        </slide>
      </carousel-3d>
    </div>
    <hr>
    <br><br><br><br>

    <!-- <div class="section">
      <div class="section-header">인기 영화</div>
      <MovieCarousel :movies="popular_movies"/>
    </div> -->
    <!-- <div class="section">
      <div class="section-header">{{ first_genre }}</div>
      <MovieCarousel :movies="first_genre_movies"/>
    </div>
    <div class="section">
      <div class="section-header">{{ secound_genre }}</div>
      <MovieCarousel :movies="secound_genre_movies"/>
    </div> -->

  </div>
</template>

<script>
import axios from 'axios'
import StarRating from 'vue-star-rating'
import { mapState } from 'vuex'

import Vue from 'vue'
import { Carousel3d, Slide } from 'vue-carousel-3d';
Vue.use('Carousel3d')

const BACKEND = process.env.VUE_APP_BACKEND_LINK
export default {
  name : 'Movies',
  components : {
    StarRating,
    Carousel3d,
    Slide,
  },
  data : function(){
    return {
      selected_movies: [],
      netflix_movies : [],
      disney_movies: [],
      hulu_movies: [],
      mvti_movies: [],
      popular_movies: [],
      // first_genre: '',
      // first_genre_movies: [],
      // secound_genre: '',
      // secound_genre_movies: [],
      slides: 15,
      slides_2d: 15,
    }
  },
  
  methods : {
    setToken: function () {
      const token = localStorage.getItem('jwt')
      const config = {
        Authorization: `JWT ${token}`,
      }
      return config
    },
    getMovies : function() {
      const link = 'movies'
      axios({
          method: 'get',
          url: BACKEND+link,
          headers: this.setToken(this.token),
      })
        .then(res =>{
          console.log(res.data.popular_movies[4].poster_path)
          console.log(res.data.netflix_movies)
          this.selected_movies = res.data.netflix_movies
          this.netflix_movies = res.data.netflix_movies
          this.disney_movies = res.data.disney_movies
          this.hulu_movies = res.data.hulu_movies
          this.mvti_movies = res.data.mvti_movies
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
      // axios.get(BACKEND+link, this.setToken(this.token))
      //   .then(res =>{
      //     console.log(res.data.popular_movies[4].poster_path)
      //     console.log(res.data.netflix_movies)

      //     this.selected_movies = res.data.netflix_movies
      //     this.netflix_movies = res.data.netflix_movies
      //     this.disney_movies = res.data.disney_movies
      //     this.hulu_movies = res.data.hulu_movies
      //     this.mvti_movies = res.data.mvti_movies
      //     this.popular_movies = res.data.popular_movies
      //     // this.first_genre = res.data.first_genre
      //     // this.first_genre_movies = res.data.first_genre_movies
      //     // this.secound_genre = res.data.secound_genre
      //     // this.secound_genre_movies = res.data.secound_genre_movies
      //   })
      //   .catch(error=> {
      //     alert(error)
      //     console.log(BACKEND+link)
      //   })
    },
    getMvtiMovies: function() {
      console.log(this.$route.params.username)
      axios({
        method: 'get',
        url: `${BACKEND}movies/mvti/`,
        headers: this.setToken(this.token)
      })
        .then(res => {
          this.mvti_movies = res.data
        })
        .catch(() => {
          alert('로그인을 하지 않았습니다.')
        })
    },
    switchSlidMovie: function(select_movie) {
      let menuLinks = document.querySelectorAll('.ott-button')
      function clickMenuHandler() {

        for (let i= 0; i< menuLinks.length; i++){
          menuLinks[i].classList.remove('button-slider-active');
          menuLinks[i].classList.add('button-slider')
        }
        this.classList.add('button-slider-active');
        this.classList.remove('button-slider')

      }
      for (let i= 0; i< menuLinks.length; i++){
        menuLinks[i].addEventListener('click', clickMenuHandler)
      }
      if (select_movie === 'mvti_movies'){
        this.getMvtiMovies()
      }
      this.selected_movies = select_movie
      
    },

    goToMovieDetail: function(movie) {
      this.$router.push({
        path: `/movies/${movie.id}`
      })
    },

  },
  created : function(){
    this.getMovies()
  },
  computed : {
    ...mapState([
      'token'
    ]),
  }
}
</script>

<style scoped>


#ott-button {
  margin-left: 10%;
}
.section {
  margin : 20px;
}

.else-movieslide {
  margin-left: 10%;
  color: #B00084;
}

.imggroup {
  position: relative;
}
.imggroup-button1 {
  position: absolute; 
  left:50%; 
  bottom: 30%; 
  margin-left:-20px;
}

.imggroup-button2 {
  position: absolute;
  left:50%; 
  bottom: 30%; 
  margin-left:-20px; 
  width: 30%;
}

.button-slider-active {
  color:#B00084;
}
.button-slider {
  color:rgba(255,255,255,.55);
}
</style>