<template>
  <div class="background-img3">
    <div class="padding">
      <h1>OTT 서비스 공유 모집 게시글</h1>
      <br><br><br>
      <div class="">
        <div class="mb-3">
          <h4 for="title" class="form-label" style="text-align:left; color:white">제목</h4>
          <input 
            v-model="recruit.title" 
            placeholder="제목을 입력해주세요." 
            type="text" 
            class="form-control" 
            id="title" 
            style="background-color:rgb(29, 26, 26); color:white; border-color:gray"
            >
        </div>
        <br><br>

        <div class="mb-3">
          <h4 for="ott_name" class="form-label" style="text-align:left; color:white">OTT 서비스명</h4>
          <input 
            v-model="recruit.ott_name" 
            placeholder="공유하고 싶은 계정의 OTT 서비스를 입력해 주세요"
            type="text"
            class="form-control" 
            id="ott_name" 
            style="background-color:rgb(29, 26, 26); color:white; border-color:gray"
            >
        </div>

        <div class="mb-3">
          <h4 for="max_cnt" class="form-label" style="text-align:left; color:white">총 공유 인원</h4>
          <input 
            v-model="recruit.max_cnt" 
            placeholder="총 계정 공유 인원을 입력해 주세요"
            type="number"
            class="form-control" 
            id="max_cnt" 
            style="background-color:rgb(29, 26, 26); color:white; border-color:gray"
            >
        </div>

        <div class="mb-3">
          <h4 for="current_cnt" class="form-label" style="text-align:left; color:white">현재 공유 인원</h4>
          <input 
            v-model="recruit.current_cnt" 
            placeholder="현재 계정을 공유하고 있는 인원을 입력해 주세요"
            type="number"
            class="form-control" 
            id="current_cnt" 
            style="background-color:rgb(29, 26, 26); color:white; border-color:gray"
            >
        </div>

        <div class="mb-3">
          <h4 for="public_id" class="form-label" style="text-align:left; color:white">공유할 계정 아이디</h4>
          <input 
            v-model="recruit.public_id" 
            placeholder="공유할 계정의 아이디(메일)를 입력해 주세요."
            type="text"
            class="form-control" 
            id="public_id" 
            style="background-color:rgb(29, 26, 26); color:white; border-color:gray"
            >
        </div>

        <div class="mb-3">
          <h4 for="public_pw" class="form-label" style="text-align:left; color:white">공유할 계정 비밀번호</h4>
          <input 
            v-model="recruit.public_pw" 
            placeholder="현재 계정을 공유하고 있는 인원을 입력해 주세요"
            type="text"
            class="form-control" 
            id="public_pw" 
            style="background-color:rgb(29, 26, 26); color:white; border-color:gray"
            >
        </div>
        
        <div class="mb-3">
          <h4 for="content" class="form-label" style="text-align:left; color:white">내용</h4>
          <textarea 
            v-model="recruit.content" 
            placeholder="내용을 입력해 주세요"
            class="form-control" 
            id="content" 
            rows="10"
            style="background-color:rgb(29, 26, 26); color:white; border-color:gray"
            >
            </textarea>
        </div>
      </div>
      <br>
      <button @click="uploadRecruit" class="btn btn-warning btn-sm m-1">저장</button>&nbsp;
      <button @click="cancle" class="btn btn-dark btn-sm m-1">취소</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import { mapState } from 'vuex'

const BACKEND = process.env.VUE_APP_BACKEND_LINK


export default {
  name:'RecruitForm',
  data (){
    return{
      recruit : {
        title:'',
        content:'',
        ott_name: '',
        max_cnt: '',
        current_cnt: '',
        public_id: '',
        public_pw: '',
      }
    }
  },
  computed : {
    ...mapState([
      'token'
    ])
  },
  methods:{
    setToken: function () {
      const token = localStorage.getItem('jwt')
      const config = {
        Authorization: `JWT ${token}`,
      }
      return config
    },

    uploadRecruit () {
      axios({
        method: 'post',
        url: `${BACKEND}recruits/create/`,
        data: this.recruit,
        headers: this.setToken(this.token),
      })
        .then(res => {
          console.log(res)
          this.$router.push({
            path:'/recruits'
          })
        })
        .catch(err => {
          console.log(err)
        })
    },
    cancle () {
      this.$router.push({
        path:'/recruit'
      })
    }
  },

}
</script>

<style>
  .background-img3 { 
    background: linear-gradient(rgba(0,0,0,0.4),rgba(0,0,0,0.6));
    background-size:cover;
    height:100vh;
    /* background-color: black; */
    background-repeat: no-repeat;
  }
</style>