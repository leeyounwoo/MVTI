<template>
	<swiper class="swiper" ref="mySwiper" 
		:options="swiperOptions" 
		@slideChange="slideChangeTransitionStart"
	> 
    
    <MoviesSliderItem v-for="(movie, idx) in movies" :key="idx" :movie="movie" :style="movie | styleSwiper"/>
		<!-- pagination -->
		<div class="swiper-pagination" slot="pagination"></div>
        
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
  name : 'MoviesSlider',
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
        effect: 'coverflow',
        grabCursor: true,
        centeredSlides: true,
        slidesPerView: 'auto',
        coverflowEffect: {
          rotate: 30,
          stretch: 0,
          depth: 200,
          modifier: 1,
          slideShadows : true,
        },
        autoplay: {
          delay: 2500,
          disableOnInteraction: true,
        },
        loop : true,
        pagination: {
          el: '.swiper-pagination'
        },
        navigation: {
          nextEl: '.swiper-button-next',
          prevEl: '.swiper-button-prev',
        },                    
      },
    }
  },
  computed : {
    swiper : function() {
				return this.$refs.mySwiper.$swiper;
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
		this.swiper.slideTo(2, 1000, false)
  }
}
</script>

<style>

.swiper-container {
  background: #262626;
  width: 100%;
  padding-top: 30px;
  padding-bottom: 50px;
}
.swiper-slide {
  background-position: center;
  background-size: cover;
  width: 500px;
  height: 600px;
  background: #fff;
  /* 반사 */
  -webkit-box-reflect : below 1px linear-gradient(transparent, transparent, #0006);
}

.swiper-slide img {
  display: block;
  width: 100%;
}

/* 경계선 */
.contentBx
{
  display : flex;
  flex-direction : column;
  justify-content: flex-end;
  text-align: center;
  transition: 1s;
  padding-bottom : 50px;
}
.contentBx h2
{
  position: absolute;
  top: 85%;
  right : 50%;
  transform : translateX(50%);
  font-weight: 600;
  letter-spacing: 1px;
  color: #fff;
  transition: 0.5s;
  mix-blend-mode : exclusion;
}
.contentBx:hover h2{
  top: 55%;
  mix-blend-mode : exclusion;
}


.contentBx .size,
.contentBx .color
{
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 8px 20px;
  transition: 0.5s;
  opacity: 0;
  visibility: hidden;
}
.contentBx:hover  .size
{
  /* opacity: 1; */
  opacity: 1;
  visibility: visible;
  transition-delay: 0.6s;
}
.contentBx:hover .color
{
  /* opacity: 1; */
  opacity: 1;
  visibility: visible;
  transition-delay: 0.5s;
}
.contentBx .size h3,
.contentBx .color h3
{
  color: #fff;
  font-weight: 300;
  font-size: 14px;
  text-transform: uppercase;
  letter-spacing: 2px;
  margin-right: 10px;
}

.swiper-slide .contentBx .color span
{
  width: 20px;
  height: 20px;
  background: #ff0;
  border-radius: 50%;
  margin: 0 5px;
  cursor: pointer;
}

.contentBx a
{
  display: inline-block;
  padding: 10px 20px;
  background: #fff;
  border-radius: 4px;
  margin-top: 10px;
  text-decoration: none;
  font-weight: 600;
  width : 100px;
  color: #111;
  margin-left : auto;
  margin-right: auto;
  opacity: 0;
  transform: translateY(50px);
  transition: 0.5s;
}
.contentBx:hover a
{
  opacity: 1;
  transform: translateY(0px);
  transition-delay: 0.75s;
}
</style>