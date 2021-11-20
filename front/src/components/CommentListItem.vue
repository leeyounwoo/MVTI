<template>
  <article class="cmt_unit" id="comment_65603837">
    
    <div class="inkpf_wrap">
      <span class="inkpf round"><Gravatar :email="comment.user.email" class="profile-img inkpf_img"/></span>					
    </div>
    <div class="cmt_header">
      <router-link :to="{name : 'Mypage', params : {username: this.comment.user.username}}"  class="nickname member_62105361" onclick="return false">{{comment.user.username}}</router-link>
      <div class="cmt_ctrl_wrap ctrl_wrap">
        <button class="bt_cmt_ctrl bt_ctrl" type="button" @click="deleteComment">
          <i class="fas fa-times"></i>
        </button>						
        <div class="cmt_ctrl ctrl_body">
          <a class="bt" href="javascript:void(0)" onclick="insertWarn('권한이 없습니다.')">
            <i class="fas fa-comment-dots"></i> 
            댓글
          </a>																				
        </div>
      </div>
    </div>
    <div class="cmt_body">
      <div class="comment_65603837_62105361 rhymix_content xe_content" data-pswp-uid="2">{{comment.content}}</div>								
      <div class="cmt_buttons"><div class="cmt_vote">

        <div class="bt_wrap" ><!--@click="likeComment"-->																						 
          <button class="text_en bt bt_vote" type="button" title="추천" >
            <VueStar animate="animate__animated animate__jackInTheBox" color="#F05654" :check="comment.like_users | checkChecked(loginUser.id)">
              <i slot="icon" class="fa fa-heart " @click="likeComment"></i>
            </VueStar>
            <span class="voted_count" style="padding-left:10px;"> {{comment.like_users.length }}</span>
          </button>
        </div>
        </div></div>
        <div class="cmt_date_wrap text_en font_grey1">
          <div class="cmt_date">{{comment.created_at | timeFor}}</div>
        </div>
    </div> 
  </article>
</template>

<script>
import axios from 'axios'
import movieMixin from "@/mixins/movieMixin"
import Gravatar from 'vue-gravatar'
import VueStar from '@/components/VueStar'

const BACKEND = process.env.VUE_APP_BACKEND_LINK
export default {
  name:'CommentListItem',
  mixins : [movieMixin],
  props: {
    comment: {
      type: Object,
    },
    loginUser : {
      type : Object,
    }
  },
  filters : {
    checkChecked : function(arr, id){
      return arr.includes(id)
    } 
  },
  methods : {
    likeComment: function () {
      axios({
        method: 'post',
        url: `${BACKEND}community/${this.comment.id}/comment/like/`,
        headers: this.setToken(this.$store.state.token)
      })
      .then(res => {
        console.log(res)
        this.$emit('deleteComment')
      })
      .catch(err => {
        console.log(err)
      })
    },
    deleteComment: function () {
      axios({
        method: 'delete',
        url: `${BACKEND}community/comment/${this.comment.id}/delete/`,
        headers: this.setToken(this.$store.state.token)
      })
      .then(res => {
        console.log(res)
        this.$emit('deleteComment')
      })
      .catch(err => {
        console.log(err.response)
        alert('해당 작성자만 삭제할 수 있습니다.')
      })
    },
    
  },
  created : function () {
    this.Commentliked = this.comment.like_users.length
  },
  components : {
    Gravatar,
    VueStar
  },

}
</script>

<style scoped>
.VueStar {
	position: absolute;
	transform: translate(-50%,-38%);
}

</style>