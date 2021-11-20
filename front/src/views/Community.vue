<template>
  <div id="background" ref="scrollTarget"> 
    <!--  @scroll="handleNotificationListScroll"  -->
    <ReviewList :reviews="reviews" />
    <div id="end" style="visibility: hidden;">리뷰 종료</div>
  </div>
</template>

<script>
import ReviewList from '@/components/ReviewList'
import axios from 'axios'
import _ from 'lodash'
const BACKEND = process.env.VUE_APP_BACKEND_LINK

export default {
  name: 'Community',
  data: function () {
    return {
      reviews: [],
      page : 1,
      dupCheck : true
    }
  },
  components : {
    ReviewList
  },
  methods : {
    isScrolledIntoView (el) {
      let rect = el.getBoundingClientRect()
      let elemTop = rect.top
      let elemBottom = rect.bottom

      let isVisible = elemTop < window.innerHeight && elemBottom >= 0
      return isVisible
    },
    scroll () {
      window.onscroll = _.throttle(() => {
        let scrolledTo = document.querySelector('#end')

        if (scrolledTo && this.isScrolledIntoView(scrolledTo)) {
          this.getData()
        }
      }, 500)
    },

    getData : function(){
      if(this.dupCheck){
        this.dupCheck=false
        console.log("페이지:"+this.page)
        axios({
          method: 'get',
          url: `${BACKEND}community/?page=${this.page}`,
        })
          .then(res => {
            console.log(res)

            this.reviews= this.reviews.concat(res.data)

            
            // this.$store.dispatch('login',res)
            // this.$router.push({ name: 'Movies'})
            // commit('LOGIN',res)
            // localStorage.setItem('jwt', res.data.token)
            // this.$emit('login')
            // this.$router.push({ name: 'Intro' })
            this.page++
            this.dupCheck = true
          })


      }
    }

  },

  created : function () {
    this.getData()
  },
  mounted () {
    this.scroll()
  }
}
</script>


<style scoped>

#background{
  background-color: #E6E6E6;
}
</style>