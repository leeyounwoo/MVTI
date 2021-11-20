<template>
  <section class="transformers-area">
    <div class="container">
      <div class="transformers-box">
        <div class="row flexbox-center">
          <div class="col-lg-5 text-lg-left text-center">
            <div class="transformers-content">
              <img :src="movie|imageURL" alt="about" />
            </div>
          </div>
          <div class="col-lg-7">
            <div class="transformers-content">
              <h2>{{ movie.title }}</h2>
              <p>{{ movie.genres | getGernres}}</p>
              <ul>
                <li>
                  <div class="transformers-left">
                    평점 :
                  </div>
                  <div class="transformers-right">
                    <StarRating :rating="parseFloat(movie.vote_average) / 2" :read-only="true" :increment="0.01"/>
                  </div>
                </li>
                <li>
                  <div class="transformers-left">
                    개봉일 :
                  </div>
                  <div class="transformers-right">
                    {{ movie.release_date }}
                  </div>
                </li>
                <li>
                  <div class="transformers-left">
                    줄거리:
                  </div>
                  <div class="transformers-right">
                    {{ movie.overview }}
                  </div>
                </li>
                
              </ul>
            </div>
          </div>
        </div>
        
        <a href="javascript:void(0)" class="theme-btn" data-bs-toggle="modal" data-bs-target="#exampleModal" v-if="token"><i class="icofont icofont-ticket"></i> 리뷰쓰기 </a>
      </div>
    </div>

<div class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
  <div class="modal-dialog modal-lg">
    <div class="modal-content">
      <div class="modal-header ">
        <h5 class="modal-title" id="exampleModalLabel">리뷰 글 작성</h5>
        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
      </div>
      <div class="modal-body" style="padding: 15px 50px;">
        <form>
          <div class="form-group">
            <label for="exampleFormControlInput1">Review Title</label>
            <input type="email" class="form-control" id="exampleFormControlInput1" placeholder="리뷰 제목" v-model="exampleDataSet.title">
          </div>
          <br>
          <div class="form-group">
            <label for="exampleFormControlTextarea1">Review Content</label>
            <textarea style="overflow-y: scroll;height: 250px; resize: none; font-size: 18px font-weight:500;" class="form-control" id="exampleFormControlTextarea1" rows="3" placeholder="리뷰 내용" v-model="exampleDataSet.content"></textarea>
          </div>
          <br>
          <div class="form-group">
            <div class="form-check">
              <input class="form-check-input" type="radio" value="true" name="liked_radio" id="defaultCheck1"  v-model="exampleDataSet.liked" >
              <label class="form-check-label" for="defaultCheck1" >
                이 영화 개꿀잼입니다.
              </label>
            </div>
            <div class="form-check">
              <input class="form-check-input" type="radio" value="false" name="liked_radio" id="defaultCheck2" v-model="exampleDataSet.liked">
              <label class="form-check-label" for="defaultCheck2">
                전 별로에요.
              </label>
            </div>
          </div>
        </form>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-light" data-bs-dismiss="modal">Close</button>
        <button type="button" class="btn btn-dark" data-bs-dismiss="modal" @click="createSubmit">Save</button>
      </div>
    </div>
  </div>
</div>
    <!-- <ReviewWrite class="modal fade" id="exampleModal" tabindex="-1" aria-hidden="true"/> -->

  </section><!-- transformers area end -->
</template>

<script>
import movieMixin from "@/mixins/movieMixin"
import StarRating from 'vue-star-rating'
// import ddForm from 'vue-dd-form';
import axios from 'axios'
import { mapActions } from 'vuex'
import { mapState } from 'vuex'
const BACKEND = process.env.VUE_APP_BACKEND_LINK
// import ReviewWrite from "@/components/ReviewWrite.vue"

export default {
  name : 'MovieDetailMain',
  
  computed : {
    ...mapState([
      'token'
    ])
  },
  created: function () {

    
  },
  components : {
    StarRating,
    // ddForm
    // ReviewWrite
  },
  data : function(){
    return {
      exampleDataSet: {
        title: '',
        content: '',
        liked: "true",
      },
    }
  },
  props : {
    movie : {
      type : [String, Object],
    },
  },
  mixins : [movieMixin],
  filters : {
    getGernres : function(genres){
      return genres.map((genre) => {
        return genre.name
      }).join(" | ")
    }
  },
  methods: {
    isLogin: function () {
      if (!this.token){
      const detailItem ={
        name: 'movies',
        params: this.$route.params.movie_pk
      }
      this.$store.dispatch('setNextPage',detailItem)
      // this.setNextPage('MovieDetail',this.$route.params.movie_pk)
      this.$router.push({name : 'Login'})
      } 
    },
    ...mapActions([
      'setNextPage'
    ]),
    setToken: function () {
      const config = {
        Authorization: `JWT ${this.$store.state.token}`
      }
      return config
    },
    createSubmit: function () {
      axios({
        method: 'post',
        url: `${BACKEND}community/${this.$route.params.movie_pk}/review/`,
        headers: this.setToken(),
				data: {
					'title':this.exampleDataSet.title,
					'content':this.exampleDataSet.content,
					'liked':this.exampleDataSet.liked
					}
      })
        .then(res => {
          console.log(res)
          // body.className =''
          this.$router.push({ name: 'Review', params:{detail: res.data.id} })
        })
        .catch(err => {
          console.log(err)
        })
    }
  },
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css?family=Poppins:300,400,500,600,700,900');
button--submit{
  visibility: hidden;
  opacity: 0;
}
h2
{
  font-size: 30px;
  font-weight: 500;
  color: #fff;
}
h2,
p {
  margin: 0px;
}
img {
  max-width: 100%;
  height: auto;
}
iframe {
  width: 100%;
  border: none;
}

ul {
  list-style: none;
  margin: 0;
  padding: 0;
}
button{
  cursor: pointer;
}
textarea {
height: 160px;
}

.section-title h1 i {
  color: #fece50;
font-size: 40px;
margin-right: 5px;
}
.mt-100 {
  margin-top: 100px;
}
.mt-30 {
  margin-top: 30px;
}
.mt-20 {
  margin-top: 20px;
}
.pt-60 {
padding-top: 60px;
}
.pb-90 {
padding-bottom: 90px;
}
.pb-20 {
padding-bottom: 20px;
}
.ptb-100 {
  padding: 100px 0;
}
.ptb-90 {
  padding: 90px 0;
}

.theme-btn {
background: #eb315a;
  border: 1px solid #eb315a;
  color: #fff;
border-radius: 35px;
  padding: 5px 25px;
  display: inline-block;
  font-size: 16px;
cursor: pointer;
font-weight: 500;
}
.theme-btn:hover {
  border: 1px solid #eb315a;
background: transparent;
  color: #eb315a;
}
.theme-btn2:hover,
.theme-btn2 {
  color: #fff;
background: #963dad; /* Old browsers */
background: -moz-linear-gradient(top, #963dad 0%, #9c3db1 34%, #ba3fc4 65%, #c340ca 100%); /* FF3.6-15 */
background: -webkit-linear-gradient(top, #963dad 0%,#9c3db1 34%,#ba3fc4 65%,#c340ca 100%); /* Chrome10-25,Safari5.1-6 */
background: linear-gradient(to bottom, #963dad 0%,#9c3db1 34%,#ba3fc4 65%,#c340ca 100%); 
border: none;
}
.flexbox-center {
  display: -moz-flex;
  display: -ms-flex;
  display: -o-flex;
  display: -webkit-box;
  display: -ms-flexbox;
  display: flex;
  -webkit-box-pack: center;
  -ms-flex-pack: center;
  justify-content: center;
  -webkit-box-align: center;
  -ms-flex-align: center;
  align-items: center;
}

/* transforemr-area */
.transformers-area {
  padding-top : 20px;
  padding-bottom : 20px;
  line-height: 24px;
  font-size: 18px;
  color: #b6b7b9;
  background: #13151f;
  font-family: 'Poppins', sans-serif;
  font-weight: 400;
  position: relative;
}

.transformers-box {
  padding: 35px;
  box-shadow: 0 0 20px #000000;
  position: relative;
}

.transformers-box .transformers-content img {
  display: block;
  position: relative;
}

.transformers-content > p {
  margin: 12px 0 30px;
  position: relative;
  padding-left: 70px;
}
.transformers-content > h2 + a.theme-btn {
  margin: 12px 10px 20px 0;
}

.transformers-content > p::before {
  position: absolute;
  content: "";
  left: 0;
  bottom: 0;
  top: 0;
  width: 55px;
  height: 2px;
  margin: auto;
  background: #eb315a;
}

.transformers-left {
  color: #eb315a;
  min-width: 100px;
}

.transformers-content ul li {
  display: flex;
  margin-top: 12px;
  font-weight: 300;
}

.transformers-right .theme-btn {
  margin: 0 8px;
padding: 2px 15px;
}

.transformers-bottom {
  display: flex;
  margin-top: 10px;
  justify-content: space-between;
}

.transformers-bottom span {
  display: block;
  color: #eb315a;
}

.transformers-bottom p {
  margin-bottom: 8px;
}
.transformers-box > .theme-btn {
  position: absolute;
  right: 0;
  bottom: 0;
  border-radius: 5px 0 0;
}
</style>