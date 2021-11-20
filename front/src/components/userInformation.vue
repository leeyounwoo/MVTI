<template>
  <div class="card">
    <div class="card-header">
      <Gravatar :email="userInformations.email" class="profile-img"/>
      <!-- <img :src="imgUrl" alt="profile Image" class="profile-img"> -->
    </div>
    <div class="card-body">
      
      <p class="full-name">{{userInformations.username}} 
        </p>
      <p class="username">{{userInformations.created_at.substring(0,10)}}</p>
      <!-- <p class="city">New York</p> -->
      <p class="desc">{{userInformations.email}}</p>
      <p><userFollow  @count="countFollow"/></p>
      
    </div>
    <div class="card-footer">
      <div class="col vr">
        <p><span class="count">{{followerCount}}</span>Followers</p>
      </div>
      <div class="col">
        <p><span class="count" id="following">{{userInformations.followers}}</span>Following</p>
      </div>
    </div>
  </div>
</template>

<script>

import axios from 'axios'
import userFollow from '@/components/userFollow'
import Gravatar from 'vue-gravatar'

const BACKEND = process.env.VUE_APP_BACKEND_LINK
export default {
  name:'userInformation',
  data: function (){
    return {
      userInformations: '',
      imgUrl: null,
      followerCount: '',
    }
  },
  methods:{
    setToken: function () {
      const config = {
        Authorization: `JWT ${this.token}`
      }
      return config
    },
    countFollow: function (data) {
      // console.log(data.count);
      const followCount =document.querySelector('#following')
      followCount.innerText =data
    }

    
  },

  created: function () {
    axios({
          method: 'get',
          url: `${BACKEND}accounts/${this.$route.params.username}`,
          headers: this.setToken()
        })
        .then(res => {
          // console.log(res)
          this.userInformations = res.data
          this.followerCount = res.data.followings
          this.imgUrl =`https://s.gravatar.com/avatar/${res.data.email_hash}?d=identicon`
        })
        .catch(err => {
          console.log(err)
        })
  },
  computed:{
    token : function () {
      return this.$store.state.token
    }
  },
  components:{
    userFollow,
    Gravatar,
  }

}
</script>

<style scoped>
* {
  box-sizing: border-box;
}

body {
  font-family: "Raleway";
  background-color: #e6e6e6;
}

.card {
  width: 400px;
  margin: auto;
  background-color: #fff;
  box-shadow: 0 3px 30px rgba(0,0,0,.14);
  color: #444;
  text-align: center;
  font-size: 16px;
}

.card .card-header {
  position: relative;
  height: 48px;
}
.card .card-header .profile-img{
  width: 96px;
  height:96px;
  border-radius: 1000px;
  position: absolute;
  left : 50%;
  transform: translate(-50%, -50%);
  border: 6px solid #fff;
  box-shadow: 0 0 20px rgba(0,0,0,.2);
}

.card .card-body {
  padding: 10px 40px;

}
.card .card-body .full-name{
  font-size:20px;
  font-weight: 600;
  text-transform: uppercase;
  margin: 10px 0 0;

}
.card .card-body .username {
  font-size: 13px;
  color:#777;
  margin: 5px 0 0;
}
.card .card-body .city {
  font-weight: 500;
  margin :10px 0 0
}

.card .card-body .desc {
  line-height: 24px;
}

.card .card-footer {
  display:table;
  width: 100%;
  border-top: 1px solid #e6e6e6;

}
.card .card-footer .col{
  display: table-cell;
  padding: 5px 10px;
  font-size: 15px;
}
.card .card-footer .count {
  font-size: 18px;
  font-weight: 600;
}

.vr {
  border-right: 1px solid #e6e6e6;
}

@media screen and (max-width: 575px) {
  .card {
    width: 96%;
  }
  .card .card-body {
    padding: 10px 20px;
  }

  .card .card-footer .col {
    padding:0 10px;
  }
  .card .card-footer .count {
    display: block;
    margin-bottom: 5px;
  }
}
</style>