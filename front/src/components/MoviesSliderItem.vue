<template>
  <!-- <img class="swiper-slide" :src="imgSrc"/> -->
  <div class="swiper-slide contentBx">
    <h2>{{ movie.title }}</h2>
    <div class="size">
      <star-rating :rating="parseFloat(movie.vote_average) / 2" :read-only="true" :increment="0.01"/>
      <!-- <span>7</span>
      <span>8</span>
      <span>9</span>
      <span>10</span> -->
    </div>
    <div class="color">
      <h3>{{ movie.release_date }}</h3>
    </div>
    <router-link :to="{name : 'MovieDetail', params : {movie_pk : movie.id }}">Detail</router-link>
  </div>
</template>

<script>
import StarRating from 'vue-star-rating'

export default {
  name : 'MoviesSliderItem',
  components : {
    StarRating
  },
  props : {
    movie : {
      type : Object
    }
  },
}
</script>

<style>

</style>