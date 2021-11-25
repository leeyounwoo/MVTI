<template>
  <div>
    <div for="" class="commentcount">댓글 작성: </div>
    <b-form-textarea
      id="textarea"
      type="text" 
      v-model.trim="newComment" 
      @keyup.enter="createComment"
      placeholder="Enter something..."
      rows="5"
      max-rows="6"
    ></b-form-textarea>
    <button @click="createComment" class="btn btn-warning btn-sm m-3">등록</button>
    <br><br><br>
    <div class="commentcount">
      {{commentCount}}개의 댓글이 있습니다.
    </div>
    <br>
    <b-list-group>
      <b-list-group-item 
        style="background-color:rgb(29, 26, 26, 0.8);  border-bottom-color:gray" 
        variant="dark" v-for="(comment) in commentSet" 
        :key="comment.id"
      >
        <div class="d-flex">
          
          <p class="indent" style="font-size:17px">&ensp;<strong>{{comment.username}}</strong></p>
        </div>
        <p>
          <strong>User{{ comment.author }}</strong> 
        </p>
        <p>{{comment.content}}</p>
        <button @click="deleteRecruitComment(comment.id)" class="btn btn-dark btn-sm">삭제</button>

      </b-list-group-item>
    </b-list-group>
    <!-- 로그인한 경우에만 댓글입력할 수 있도록 구현하기-->
    <br><br><br>
    
  </div>
</template>

<script>
import axios from 'axios'
import Vue from 'vue'
import { BFormTextarea, BListGroup, BListGroupItem } from 'bootstrap-vue'
Vue.component('b-form-textarea', BFormTextarea)
Vue.component('b-list-group', BListGroup)
Vue.component('b-list-group-item', BListGroupItem)

export default {
  name:'RecruitDetailComment',
  props:{
    commentSet :{
      type:Array
    },
    commentCount:{
      type:Number
    },
    recruitId:{
      type:Number
    }
  },
  data() {
    return {
      newComment:'',
    }
  },
  methods: {
    setToken: function () {
      const token = localStorage.getItem('jwt')
      const config = {
        Authorization: `JWT ${token}`,
      }
      return config
    },
    createComment: function () {
      const Comment = {
        content: this.newComment,
      }
      axios({
        method:'post',
        url: `http://127.0.0.1:8000/recruits/${this.recruitId}/comment/create/`,
        data: Comment,
        headers: this.setToken(this.token),
      })
        .then(res => {
          console.log(res)
          this.newComment = ''
          this.$emit('new-comment')
          console.log(res)
        })
        .catch(err => {
          console.log(err)
        })
    },
    deleteRecruitComment(commentId) {
      axios({
        method:'delete',
        url: `http://127.0.0.1:8000/recruits/${this.recruitId}/comment/delete/${commentId}`,
        headers: this.setToken(),
      })
        .then(() =>{
          this.$emit('comment-delete')
        })
        .catch(() => {
          alert('작성자가 아닙니다')
        })     
    }
  }

}
</script>

<style>
  .commentcount{
    text-align: left;
  }
  p.indent{ padding-left: 0.8em }
</style>