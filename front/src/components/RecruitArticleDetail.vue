<template>
  <div class="background-img2 padding2">
    <div class="container p-5 box" style="overflow:auto">
        <h3><strong>{{ recruit.title }}</strong></h3>
        <br>
        <h5>작성자 : {{ recruit.authorname }}님</h5>
        <br>
        <p>모집인원 : {{recruit.current_cnt}}/{{recruit.max_cnt}}</p>
        <button class='btn btn-warning m-1' @click="pay(recruit.id)">카카오페이 결제</button>
        <br>
        <hr>
        <p >내용: {{ recruit.content }}</p>
        <br>
        <hr>
        <button v-if="recruit.author == user" @click="deleteRecruitDetail" class="btn btn-dark m-1">삭제</button>
        <br><br><hr>
        <RecruitDetailComment 
          :commentCount="recruit.comment_count"
          :commentSet="recruit.comment_set"
          :recruitId ="recruit.id"
          @new-comment="getRecruitDetail"
          @comment-delete="getRecruitDetail"
        />
    </div>
  </div>
</template>

<script>
import RecruitDetailComment from '@/components/RecruitDetailComment'
import axios from 'axios'

export default {
  name:'RecruitListDetail',
  components:{
    RecruitDetailComment
  },
  data () {
    return {
      recruit:{},
    }
  },
  methods:{
    setToken: function () {
      const token = localStorage.getItem('jwt')
      const config = {
        Authorization: `JWT ${token}`,
      }
      return config
    },
    getRecruitDetail: function () {
      axios({
        method:'get',
        url: `http://127.0.0.1:8000/recruits/${this.$route.params.recruitId}/`,
        headers: this.setToken(this.token),
      })
        .then(res =>{
          this.recruit = res.data
          console.log(res)
        })
        .catch(err => {
          // console.log(recruitId)
          console.log(err)
        })
    },
    deleteRecruitDetail: function () {
      axios({
        method:'delete',
        url: `http://127.0.0.1:8000/recruits/delete/${this.$route.params.recruitId}/`,
        headers: this.setToken(),
      })
        .then(() =>{
          this.$router.push({name:'Recruit'})
        })
        .catch(() => {
          alert('작성하신 글이 아닙니다.')
        })
    },
    goUpdateForm: function () {
      axios({
        method:'get',
        url: `http://127.0.0.1:8000/recruits/update/${this.$route.params.recruitId}/`,
        headers: this.setToken(),
      })
        .then((res) =>{
          console.log(res)
        })
        .catch(() => {
          alert('작성하신 글이 아닙니다.')
        })
    },
    pay:function(recruitId){
            let baseUrl = "http://127.0.0.1:8000/"
            // let form = new FormData()
            this.$route.params.recruitId
            axios({
              method:'post',
              url: baseUrl+`recruits/${recruitId}/pay/`,
              headers: this.setToken(this.token),
            })      
            .then(res =>{
                let payUrl = res.data.next_redirect_pc_url
                console.log(res)
                location.href = payUrl
            })
            .catch(() =>{
                alert("에러가 발생했습니다!")
            })
        },
  },
  created () {
    console.log('temp')
    this.getRecruitDetail()
  },
  computed: {
    contentText: function () {
      return this.recruit.content.replace(/\n/g, '<br />');
    }
  }
}
</script>

<style>
  h3 {
    color: white;
    text-align: left;
  }
  h5 {
    color: white;
    text-align: left;
  }
  p {
    color: white;
    text-align: left;
  }
  .box {
    background-color: rgb(0, 0, 0, 0.4);
    
    border-style: solid;
    /* border-color: rgb(54, 51, 51); */
    border-radius: 10px;
    height:95%;
  }
  .background-img { 
    background: linear-gradient(rgba(0,0,0,0.3),rgba(0,0,0,0.5));
    background-color: black;
    background-size:cover;
    height:100vh;
    background-repeat: no-repeat;
  }
  .padding2 {
    padding:3% 3% 0% 3% ;
  }

</style>