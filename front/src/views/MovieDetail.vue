<template>
  <div id="container">
    <MovieDetailMain :movie="movie"/>
    <iframe width="100%" height="700px" :src="movie | videoURL" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
    <div class="section">
      <div class="section-header">비슷한 장르 영화 추천</div>
      <MovieCarousel :movies="same_genres"/>
    </div>
  </div>
</template>

<script>
import MovieDetailMain from '@/components/MovieDetailMain.vue'
import MovieCarousel from '@/components/MovieCarousel.vue'
import axios from 'axios'

const BACKEND = process.env.VUE_APP_BACKEND_LINK


export default {
  name : 'MovieDetail',
  components : {
    MovieDetailMain,
    MovieCarousel,
  },
  data : function(){
    return {
      movie : '',
      same_genres : ''
    }
  },
  methods : {
    getMovie : function(){
      const url = BACKEND + 'movies/detail/' + this.$route.params.movie_pk
      console.log(url)
      axios.get(url)
        .then((res) => {
          console.log(res)
          this.movie = res.data['movie'][0]
          this.same_genres = res.data.same_genres
        })
        .catch(() => {
          alert("없는 영화 정보입니다.")
          this.$router.push({name : 'Movies'})
        })
    }
  },
  filters : {
    videoURL : function(movie) {
      const youtubeURL = "https://www.youtube.com/embed/"
      return youtubeURL+movie.video_path
    }
  },
  created : function(){
    this.getMovie()
  }
}
</script>

<style scoped>
#container {
 background: #13151f;
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