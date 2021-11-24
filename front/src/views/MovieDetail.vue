<template>
  <div id="container">
    <div slot="body">
      <div class="d-flex">
        <div>
          <img 
            :src="`https://image.tmdb.org/t/p/original${movie.poster_path}`" 
            width="380px" alt="image">
        </div>
        <div class="padding-7 text-left">
          <h1 class="pt-3"><strong>{{movie.title}}</strong></h1>
          <h4 class="pt-1 pb-4">
            <span>개봉일: {{movie.released_date}}</span>
            평점: {{movie.vote_average}}
          </h4>
          <p class="text-size">{{movie.overview}}</p>

          <hr>
          <br>
          <div class="p-3">
            <h2><strong>영화 한줄평</strong></h2>
            <ul v-for="review in movie.review_set" :key="review.id">
              <span class="m-2">
                <span class="h5 m-2">{{review.content}}</span>
                  <span>
                    <span class="text-warning" >
                      <i v-if="review.rating < 2" class="far fa-star"></i> 
                      <i v-else class="fas fa-star"></i>
                    </span>
                    <span class="text-warning">
                      <i v-if="review.rating < 4" class="far fa-star"></i> 
                      <i v-else class="fas fa-star"></i>
                    </span>
                    <span class="text-warning">
                      <i v-if="review.rating < 6" class="far fa-star"></i> 
                      <i v-else class="fas fa-star"></i>
                    </span>
                    <span class="text-warning">
                      <i v-if="review.rating < 8" class="far fa-star"></i> 
                      <i v-else class="fas fa-star"></i>
                    </span>
                    <span class="text-warning">
                      <i v-if="review.rating < 10" class="far fa-star"></i> 
                      <i v-else class="fas fa-star"></i>
                    </span>
                  </span>
                <button class="btn btn-outline-warning btn-sm" @click="deleteMovieReviewomment(review.id, movie.id)">삭제</button>  
              </span>
            </ul>

            <div class="mx-auto">
              <div>
                <input type="text" v-model.trim="reviewInput" id="" placeholder="댓글을 입력하세요">
                <span class="big-star m-2">
                  <span @click="giveStarRating(2)" class="text-warning">
                    <i v-if="score < 2" class="far fa-star"></i> 
                    <i v-else class="fas fa-star"></i>
                  </span>
                  <span @click="giveStarRating(4)" class="text-warning">
                    <i v-if="score < 4" class="far fa-star"></i> 
                    <i v-else class="fas fa-star"></i>
                  </span>
                  <span @click="giveStarRating(6)" class="text-warning">
                    <i v-if="score < 6" class="far fa-star"></i> 
                    <i v-else class="fas fa-star"></i>
                  </span>
                  <span @click="giveStarRating(8)" class="text-warning">
                    <i v-if="score < 8" class="far fa-star"></i> 
                    <i v-else class="fas fa-star"></i>
                  </span>
                  <span @click="giveStarRating(10)" class="text-warning">
                    <i v-if="score < 10" class="far fa-star"></i> 
                    <i v-else class="fas fa-star"></i>
                  </span>
                </span>
                <button class="btn btn-warning" type="button" @click="reviewCreate(movie.id)">작성</button>      
              </div>
            </div>
            
          </div>


        </div>
      </div>
      <div class="">
        <h2 class="else-movieslide">비슷한 컨텐츠</h2><hr>
        <carousel-3d :disable3d="true" :space="230" :clickable="false" :controls-visible="true" :width="200" :height="270" :autoplay="true" :autoplay-timeout="3000">
          <slide v-for="(slide_2d, i) in slides_2d" :key="i" :index="i">
            <img 
              :src="`https://image.tmdb.org/t/p/original${similar_movies[i].poster_path}`" 
              alt="poster" 
              style="width:100%; height:100%; cursor: pointer;" 
              class="imggroup"
            >
            <star-rating v-bind:star-size="30" style="position: absolute; top: 0px; text-align: center; size: 50%;}" :rating="parseFloat(similar_movies[i].vote_average) / 2" :read-only="true" :increment="0.01"/>
              <button 
                class="imggroup-button2"
                @click="goToMovieDetail(similar_movies[i])"
              >Detail</button>
          </slide>
        </carousel-3d>
      </div>


    </div>
    
  </div>
</template>

<script>

import axios from 'axios'
import StarRating from 'vue-star-rating'
import Vue from 'vue'
import { Carousel3d, Slide } from 'vue-carousel-3d';
import { mapState } from 'vuex'

Vue.use('Carousel3d')

const BACKEND = process.env.VUE_APP_BACKEND_LINK


export default {
  name : 'MovieDetail',
  components : {
    StarRating,
    Carousel3d,
    Slide,
  },
  data : function(){
    return {
      reviewInput: '',
      score: 0,
      movie : '',
      similar_movies : [],
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
    getMovie : function(){
      const url = BACKEND + 'movies/detail/' + this.$route.params.movie_pk
      console.log(url)
      axios.get(url)
        .then((res) => {
          console.log(res)
          this.movie = res.data['movie'][0]
          // this.similar_movies = res.data.similar_movies
        })
        .catch(() => {
          alert("없는 영화 정보입니다.")
          this.$router.push({name : 'Movies'})
        })
    },
    goToMovieDetail: function(movie) {
      this.$router.push({
        path: `/movies/${movie.id}`
      })
    },
    reviewCreate: function (movieId) {
      const reviewInfo = {
        content: this.reviewInput,
        rating: this.score,
      }
      console.log(reviewInfo)
      console.log(`${BACKEND}movies/${movieId}/review/create/`)
      axios({
        method: 'post',
        url: `${BACKEND}movies/${movieId}/review/create/`,
        data: reviewInfo,
        headers: this.setToken(this.token),
      })
        .then(()=>{
          console.log('댓글작성성공')
          this.getMovie(movieId)
          // console.log(this.movie.review_set)
          this.reviewInput = ''
          this.score = 0
        })
        .catch(() => {
          alert('댓글을 입력해주세요')
        })
    },
    giveStarRating (num) {
      this.score = num
    },
  
  },
  created : function(){
    this.getMovie()
  },
  computed : {
    ...mapState([
      'token'
    ])
  },
}
</script>

<style scoped>
#container {
 background: #13151f;
}


</style>