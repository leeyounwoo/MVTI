<template>
  <div class="background-img padding">
    <div class="overflow-auto">
      <h1>OTT 모집 게시판</h1>
      <br><br>
      <b-table 
        striped 
        hover
        :items="recruits"
        :fields="fields"
        :per-page="perPage"
        :current-page="currentPage"
        @row-clicked="rowClick"
        dark
        responsive
        style="cursor: pointer;"
      ></b-table>

      <button @click="writeContent" class="btn btn-warning btn-writing">글쓰기</button>
      <br><br>
      <b-pagination
        v-model="currentPage"
        pills :total-rows="rows"
        :per-page="perPage"
        aria-controls="my-table"
        align="center"
        class="customPagination"
      ></b-pagination>
    </div>
  </div>
</template>

<script>
import Vue from 'vue'
import { BPagination, BTable } from 'bootstrap-vue'
Vue.component('b-pagination', BPagination)
Vue.component('b-table', BTable)
import axios from 'axios'
import { mapState } from 'vuex'
import { mapActions } from 'vuex'


const BACKEND = process.env.VUE_APP_BACKEND_LINK

export default {
  name : "RecruitsList",
  data: function() {
    return {
      perPage: 10,
      currentPage: 1,
      recruits : [
      ],
      fields: [
        {
          key: 'ott_name',
          label:'OTT 서비스'
        },
        {
          key: 'current_cnt',
          label:'남은 모집 인원'
        },
        {
          key: 'title',
          label: '제목',
        },
        {
          key: 'authorname',
          label: '작성자',
        },
      ],
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

    ...mapActions([
      'setNextPage'
    ]),
    getRecruits: function () {
      axios({
        method: 'get',
        url: `${BACKEND}recruits`,
        headers: this.setToken(this.token),
      })
        .then(res => {
          console.log(res)
          this.recruits = res.data
        })
        .catch(err => {
          console.log(err)
        })
    },
    rowClick (recruit){
      this.$router.push({
        path:`recruits/${recruit.id}`
      })
    },
    writeContent() {
      this.$router.push({
        path:`/recruits/create`,
      })
    },
  },
  created : function(){
    console.log('temp')
    this.getRecruits()
  },
  
  computed: {
    rows() {
      return this.recruits.length
    },
    ...mapState([
      'token'
    ])
  }
  
}
</script>

<style>
  .background-img { 
    background: linear-gradient(rgba(0,0,0,0.3),rgba(0,0,0,0.5));
    background-color: black;
    background-size:cover;
    height:100vh;
    background-repeat: no-repeat;
  }
  .padding {
    padding: 5% 15% ;
  } 
  .btn-writing {
    /* color: #8A2BE2; */
    color: #000;
    background-color: #8A2BE2;
    border-color: #8A2BE2;

  }

</style>