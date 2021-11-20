<template>
  <section>
    <div class="container">
      <div class="user signinBx">
        <div class="imgBx"><img src="../assets/login/lock.jpg" alt="lockimg"></div>
        <div class="formBx">
          <form v-on:submit.prevent="login">
            <h2>Sign In</h2>
            <input type="text" placeholder="Username" id="loginUsername" v-model="credentials.username">
            <input type="password" placeholder="Password" id="loginPassword" v-model="credentials.password">
            <input type="submit" placeholder="login" @click="login">
            <p class="signup">don't have an account? 
              <a href="javascript:void(0);" @click="toggleForm">Sign up.</a>
            </p>
          </form>
        </div>
      </div>

      <div class="user signupBx">
        <div class="formBx">
          <form v-on:submit.prevent="">
            <h2>Create an account</h2>
            <input type="text" placeholder="Username" id="createUsername" v-model="credentials.username">
            <input type="text" placeholder="Email Address" id="createEmail" v-model="credentials.email">
            <input type="password" placeholder="create Password" id="createPassword" v-model="credentials.password">
            <input type="password" placeholder="Confirm Password" id="createPasswordConfirmation" v-model="credentials.passwordConfirmation">
            <input type="submit" placeholder="Sign Up" @click="signup(credentials)" @keyup.enter="signup(credentials)">
            <p class="signup">Already have an account? 
              <a href="javascript:void(0);" @click="toggleForm">Sign in.</a>
            </p>
          </form>
        </div>
        <div class="imgBx"><img src="../assets/login/signup.jpg" alt="signupimg"></div>
      </div>
    </div>
  </section>

</template>

<script>
import axios from 'axios'
import _ from 'lodash'
import { mapState } from 'vuex'
import { mapActions } from 'vuex'
import movieMixin from "@/mixins/movieMixin"

const BACKEND = process.env.VUE_APP_BACKEND_LINK

export default {
  name : 'Login',
  data: function () {
    return {
      credentials: {
        username: null,
        email:null,
        password: null,
        passwordConfirmation: null,
        
      },
    }
  },
  mixins : [movieMixin],
  props : {
    isToggle : {
      type:Boolean
    }
  },

  computed : {
    ...mapState([
      'nextPage',
      'nextparams'
    ])
  },
  methods: {
    ...mapActions([
      'setNextPage'
    ]),
    login: function (event) {
      event.preventDefault()
      const loginItem = {
        username: this.credentials.username,
        password: this.credentials.password,
      }
      if (_.trim(this.credentials.username)){
        axios({
          method: 'post',
          url: `${BACKEND}accounts/login/`,
          data: loginItem
        })
        .then(res => {
          console.log(res)
          this.$store.dispatch('login',res)
          // nextPage가 있다면 보내주기
          if (this.nextPage){
            if (this.nextparams){
              this.$router.push(`${this.nextPage}/${this.nextparams}`)
              this.setNextPage('')
            }else {
              this.$router.push({ name: this.nextPage ,})
              this.setNextPage('')

            }
          }else{
            this.$router.push({ name: 'Movies'})
          }
        })
        .catch(err => {
          alert(this.errorMessage(err.response))
        })
        
      }
      
      this.username=''
      this.password=''
      
    },
    signup: function () {
      axios({
        method: 'post',
        url: `${BACKEND}accounts/signup/`,
        data: this.credentials,
      })
        .then(res => {
          console.log(res)
          this.credentials.username=''
          this.credentials.password=''
          this.toggleForm()
          
        })
        .catch(err => {
          alert(this.errorMessage(err.response))
        })
    },
    toggleForm : function (){
      
      const container = document.querySelector('.container');
      const section = document.querySelector('section');
      container.classList.toggle('active');
      section.classList.toggle('active');
    },


  },
  created : function (){
    if (this.$store.state.token){
      this.$router.push({name : 'Movies'})
    }
  }

}

</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@200;300;400;500;600;700;800;900&display=swap');
*
{
  margin:0;
  padding:0;
  box-sizing: border-box;
  font-size: 'Poppins',sans-serif;
}
section
{
  position: relative;
  min-height: 100vh;
  background:#557085;
  display:flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
  transition: 0.5s;
}
section.active
{
  background:#c1bfc7;

}
section .container
{
 position: relative;  
 width: 800px;
 height: 500px;
 background: #fff;
 box-shadow: 0 15px 50px rgba(0,0,0,0.1); 
 overflow: hidden;
}
section .container .user
{
  position: absolute;
  top:0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
}
section .container .user .imgBx
{
  position: relative;
  width: 50%;
  height: 100%;
  transition: 1s;
}
section .container .user .imgBx img
{
  
  position: absolute;
  top:0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
}
section .container .user .formBx
{
  position: relative;
  width: 50%;
  height: 100%;
  background: #fff;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 40px;
  transition: 1s;
}
section .container .user .formBx h2
{
  font-size: 18px;
  font-weight: 600; 
  text-transform: uppercase;
  letter-spacing: 2px;
  text-align: center;
  width:100%;
  margin-bottom: 10px;
  color: #555;
}
section .container .user .formBx input
{
  width: 100%;
  padding: 10px;
  background: #f5f5f5;
  color: #333;
  border: none;
  outline: none;
  box-shadow: none;
  font-size: 14px;
  margin: 8px 0;
  letter-spacing:1px;
  font-weight: 300;
}
section .container .user .formBx input[type="submit"]
{
  max-width: 100px;
  background: #677eff;
  color: #fff;
  cursor:pointer;
  font-size: 14px;
  font-weight: 500;
  letter-spacing: 1px;
  transition: 0.5s;
}
section .container .user .signupBx .formBx input[type="submit"]
{
  background: #e73e49;
}
section .container .user .formBx .signup
{
  position: relative;
  margin-top:20px;
  font-size: 12px;
  letter-spacing: 1px;
  color: #555;
  text-transform: uppercase;
  font-weight: 300;
}
section .container .user .formBx .signup a
{
  font-weight: 600;
  text-decoration: none;
  color:#577eff;
}
section .container .user .formBx .signupBx
{
  font-weight: 600;
  text-decoration: none;
  color: #577eff;
}
section .container .signupBx
{
  pointer-events: none;
}
section .container.active .signupBx
{
  pointer-events: initial;
}
section .container .signupBx .formBx
{
  top:100%;
}
section .container.active .signupBx .formBx
{
  top:0;
}
section .container .signupBx .imgBx
{
  top:-100%;
  transition: 1s;
}
section .container.active .signupBx .imgBx
{
  top:0;
}

section .container .signinBx .formBx
{
  top:0;
}
section .container.active .signinBx .formBx
{
  top:100%;
}

section .container .signinBx .imgBx
{
  top:0;
  transition: 1s;
}
section .container.active .signinBx .imgBx
{
  top:-100%;
}

@media (max-width: 991px)
{
  section .container
  {
    max-width: 400px;
  }
  section .container .imgBx
  {
    display: none;
  }
  section .container .user .formBx
  {
    width: 100%;
  }
  section .container.active .signinBx .formBx
  {
    top: -100%;
  }
}
</style>