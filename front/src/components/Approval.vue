<template>
  <!-- <div>
    <h1>안ㄴㄴㄴㄴ</h1>
  </div> -->
  <div class="mt-5 pt-5 row justify-content-center">
    <h2 class="text-center my-5 col-12">결제가 완료되었습니다!</h2>
    <div class="col-4 p-5 bg-dark">
      <h3 class="text-center my-5">주문 정보</h3>
      <div>
        <div class="my-3 row"><div class="h5 col-6">결제금액</div><div class="h6 col-6 text-right">{{ money }}원</div></div>
        <div class="my-3 row"><div class="h5 col-6">OTT 서비스</div><div class="h6 col-6 text-right">{{ ott }}</div></div>
        <div class="my-3 row"><div class="h5 col-6">공유 ID</div><div class="h6 col-6 text-right">{{ id }}</div></div>
        <div class="my-3 row"><div class="h5 col-6">공유 PW</div><div class="h6 col-6 text-right">{{ pw }}</div></div> 
      </div>
      <div class="mt-5 pt-3 text-center">
        <router-link :to="{name: 'Movies'}" class="btn btn-warning">메인으로 이동</router-link>
      </div>
    </div>

  </div>
</template>

<script>
import axios from 'axios'

export default {
  name : 'Approval',
  data : function(){
    return {
      money:0,
      id: '',
      pw: '',
      ott: '',
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
    approve : function() {
      let baseUrl = "http://127.0.0.1:8000/recruits/"
      axios({
        method: 'post',
        url: baseUrl+`${this.$route.params.recruitId}/pay/approval/`,
        headers: this.setToken(this.token)
      })
        .then((res) => {
          console.log('성공')
          this.money = res.data.money
          this.id = res.data.id
          this.pw = res.data.pw
          this.ott = res.data.ott
        })
        .catch(() => {
          alert('X')
        })
    },
  },
  created : function(){
    this.approve()
  }
}
</script>

<style scoped>

.main {
  background : #262626;
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
.else-movieslide {
  color: #8A2BE2;
}
</style>