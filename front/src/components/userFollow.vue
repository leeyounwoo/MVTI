<template>
  <span>
    <span class="heart-btn" v-if="isUser">
      <span class="content" @click="heart">
        <span class="heart" @click="follow"></span>
        <!-- <span class="text" @click="heart">Like</span> -->
        <!-- <span class="numb"@click="heart"></span> -->
      </span>
    </span>
  </span>
</template>

<script>
import jwt_decode from "jwt-decode";
import axios from 'axios'
const BACKEND = process.env.VUE_APP_BACKEND_LINK
export default {
  name: 'userFollow',
  data: function () {
    return {
      isActive:'heart-active',
      isUser: null,
    }
  },
  methods:{
    setToken: function () {
      const config = {
        Authorization: `JWT ${this.$store.state.token}`
      }
      return config
    },
    follow: function () {
      axios({
          method: 'post',
          url: `${BACKEND}accounts/follow/${this.$route.params.username}/`,
          headers: this.setToken()
        })
        .then(res => {
          // console.log(res)
          const content = document.querySelector('.content')
          const heart = document.querySelector('.heart')
          if (!res.data.follow){
            content.setAttribute('class','content heart-active')
            heart.setAttribute('class','heart heart-active')
          } else{
            content.setAttribute('class','content')
            heart.setAttribute('class','heart')
          }
          // console.log(res.data.count);
          this.$emit('count',res.data.count)


        })
        .catch(err => {
          // console.log('안된다고?');
          console.log(err)
        })
    }, 
  },
  created: function (){
    const decoded = jwt_decode(this.$store.state.token)
    // console.log(decoded);
    const pagename = this.$route.params.username
    const username = decoded.username
    // console.log(pagename);
    // console.log(username);
    if (pagename === username){
      this.isUser = false
    } else {
      this.isUser =true
    }
  }
}
</script>

<style scoped>
  @import url('https://fonts.googleapis.com/css?family=Montserrat:600&display=swap');
.heart-btn{
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%,200%);
}
.content{
  padding: 13px 16px;
  display: flex;
  border: 2px solid #eae2e1;
  border-radius: 5px;
  cursor: pointer;
}
.content.heart-active{
  border-color: #f9b9c4;
  background: #fbd0d8;
}
.heart{
  position: absolute;
  background: url("../assets/follow/follow.png") no-repeat;
  background-position: left center;
  background-size: 2900%;
  height: 90px;
  width: 90px;
  top: 50%;
  left: 44%;
  transform: translate(-48%,-50%);
}
.text{
  font-size: 21px;
  margin-left: 30px;
  color: grey;
  font-family: 'Montserrat',sans-serif;
}
.numb:before{
  content: '12';
  font-size: 21px;
  margin-left: 7px;
  font-weight: 600;
  color: #9C9496;
  font-family: sans-serif;
}
.numb.heart-active:before{
  content: '13';
  color: #000;
}
.text.heart-active{
  color: #000;
}
.heart.heart-active{
  animation: animate .8s steps(28) 1;
  background-position: right;
}
@keyframes animate {
  0%{
    background-position: left;
  }
  100%{
    background-position: right;
  }
}

</style>