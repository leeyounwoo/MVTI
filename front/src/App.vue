<template>
  <div id="app">
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark" id="nav1">
      <div class="container-fluid">
        <router-link :to="{name: 'Movies'}" class="navbar-brand navbar_homelogo">MVTI</router-link>

        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavDropdown" aria-controls="navbarNavDropdown" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse justify-content-end" id="navbarNavDropdown">
          <ul class="navbar-nav">
            <!-- 로그인시 보이는 것 -->
            <span class="navbar-nav" v-if="token">
              <li class="nav-item">
                <router-link :to="{name: 'Tournament'}" class="nav-link active">이상형 월드컵</router-link>
              </li>
              <li class="nav-item">
                <router-link :to="{name: 'Recruit'}" class="nav-link active">OTT모집</router-link>
              </li>
              <li class="nav-item">
                <router-link :to="`/mypage/${username}`" class="nav-link active">마이페이지</router-link>
              </li>
              <li class="nav-item">
                <router-link to="javascript:void(0)" class="nav-link active" @click.native="logout">로그아웃</router-link>
              </li>
            </span>
            <!--  로그아웃 시 보이는 것 -->
            <span class="navbar-nav" v-else>
              <li class="nav-item">
                <router-link :to="{name: 'Tournament'}" class="nav-link active">이상형 월드컵</router-link>
              </li>
              <li class="nav-item">
                <router-link :to="{name: 'Recruit'}" class="nav-link active">OTT모집</router-link>
              </li>
              <li class="nav-item" >
                <router-link :to="{name: 'Login'}" class="nav-link active">Login</router-link>
              </li>
            </span>
          </ul>
        </div>
      </div>
    </nav>

    <router-view :key="$route.fullPath"/>
  </div>
</template>
<script>
import jwt_decode from "jwt-decode";
import Vue from 'vue'
import { BButton, BSidebar } from 'bootstrap-vue'
Vue.component('b-button', BButton)
Vue.component('b-sidebar', BSidebar)

export default {
  
  name: 'App',
  data: function () {
    return {
      isTrue: true,
    }
  },
  methods:{
    logout : function (){
      this.$store.dispatch('logout')
      this.$router.push({name : 'Login' })
    },
  },
  computed:{
    token : function () {
      return this.$store.state.token
    },
    username : function(){
      return jwt_decode(this.token).username
    }
  },
}
</script>

<style scoped>
#app {
  color: #2c3e50;
}

#nav {
  padding: 30px;
}



#nav1 .router-link-exact-active {
  color: #B00084;
  font-weight: bold;
}

.navbar-nav .nav-item{
  text-align:center;
}

.navbar_homelogo {
  font-size: 50px;

}
</style>

