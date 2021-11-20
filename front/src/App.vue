<template>
  <div id="app">
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
      <div class="container-fluid">
        <router-link :to="{name: 'Movies'}" class="navbar-brand">MOYA</router-link>

        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavDropdown" aria-controls="navbarNavDropdown" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse justify-content-end" id="navbarNavDropdown">
          <ul class="navbar-nav">
            <!-- 로그인시 보이는 것 -->
            <span class="navbar-nav" v-if="token">
              <li class="nav-item">
                <router-link :to="`/tournament`" class="nav-link active">영화월드컵</router-link>
              </li>
              <li class="nav-item">
                <router-link :to="{name: 'Community'}" class="nav-link active">커뮤니티</router-link>
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
                <router-link :to="{name: 'Community'}" class="nav-link active">커뮤니티</router-link>
              </li>
              <li class="nav-item" >
                <router-link :to="{name: 'Login'}" class="nav-link active">Login</router-link>
              </li>
              <!-- <li class="nav-item">
                <router-link :to="{name: 'Login'}" class="nav-link active" :isToggle="isTrue">Signup</router-link>
              </li> -->
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
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  /* text-align: center; */
  color: #2c3e50;
}

#nav {
  padding: 30px;
}

#nav a {
  font-weight: bold;
  color: #2c3e50;
}

#nav a.router-link-exact-active {
  color: #42b983;
}

.navbar-nav .nav-item{
  text-align:center;
}
</style>

