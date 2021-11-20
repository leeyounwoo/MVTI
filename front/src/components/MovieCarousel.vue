<template>

	<swiper class="swiper" ref="mySwiper2" 
		:options="swiperOptions" 
		@slideChange="slideChangeTransitionStart"
	> 
    
    <MoviesSliderItem v-for="(movie, idx) in movies" :key="idx" :movie="movie" :style="movie | styleSwiper"/>
		<!-- pagination -->

	</swiper>

</template>

<script>
import Vue from 'vue'
import VueAwesomeSwiper from 'vue-awesome-swiper'
import 'swiper/css/swiper.css'
Vue.use(VueAwesomeSwiper);

import {Swiper, } from 'vue-awesome-swiper'
import MoviesSliderItem from '@/components/MoviesSliderItem'

export default {
  name : 'MovieCarousel',
  components : {
    Swiper,
    MoviesSliderItem,

  },
  props : {
    movies : {
      type : Array,
    },
  },
  data : function(){
    return {
      swiperOptions: {
        slidesPerView: 3,
        spaceBetween: 30,
        freeMode: true,
        mousewheel : true,

      },
    }
  },
  computed : {
    swiper : function() {
				return this.$refs.mySwiper2.$swiper;
    }
  },
  methods : {
    slideChangeTransitionStart : function() {
      console.log(this.swiper.activeIndex); //현재 index값 얻기
    }
  },
  filters : {
    styleSwiper : function(movie){
      return "background-image:url("+"https://image.tmdb.org/t/p/w500"+movie.poster_path+")"
    }
  },
  mounted() {
			//console.log('Current Swiper instance object', this.swiper)
		this.swiper.slideTo(1, 1000, false)
  }
}

</script>

<style>

</style>