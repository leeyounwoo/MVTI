<template>
  <div class="ink_wrap lightmode" style="padding-bottom:189px;">
	<div id="container" class="ink_container header_typeB3 containerN">
	<div id="ink_wrapper" class="ink_wrapper">
	<div id="content" class="ink_content">
	<section class="ink_board guest_mode">

  <article class="ink_atc round20 has_list ">
		<!-- 글제목 부분 -->
		<header class="atc_header">
			<h1>
				<a href="javascript:void(0)" class="atc_title">{{detail.title}}</a>
			</h1>
			<div class="atc_info clearfix">
				<span class="atc_nickname">
				<span class="inkpf color round small"><Gravatar :email="detail.user.email" class="profile-img inkpf_img"/></span>
					<router-link :to="{name : 'Mypage', params : {username: this.detail.user.username}}">{{detail.user.username}}</router-link>
        </span>
				<span class="text_en atc_date font_grey1"><time datetime="2021-05-22T18:05:58+09:00">{{ detail.created_at | timeFor }}</time></span>
				<div class="atc_info_right text_en font_grey1">				
					<span class="count_vote pt_col"><i class="fas fa-heart" title="추천 수"></i> {{like_users.length + funny_users.length +helpful_users.length }}</span>		 		
					<span class="count_cmt pt_col2"><i class="fas fa-comment-dots" tilte="댓글"></i> {{detail.comment_count}}</span>
				</div>
			</div>
		</header>
    
		<div class="atc_body">
		  <!-- 글 내용 부분 -->
			<div class="document_65603779_42982247 rhymix_content xe_content" data-pswp-uid="1">
				<p>
					<img :src="detail.movie|imageURL" alt="movie_poster" data-pswp-pid="1" @click="$router.push(`/movies/${detail.movie.id}`)">
				</p>
        <br>
				<p>{{detail.content}}</p>
			</div>
      <br>
      <br>

			<!-- 좋아요 및 버튼부분 -->
			<div class="atc_buttons clearfix ">
				<span class="atc_vote " >
						<button class="bt_vote vote_area " type="button">
							   <VueStar animate="animate__animated animate__jackInTheBox" color="#F05654" :check="like_users | checkChecked(login_user.id)" >
    								<i slot="icon" class="fa fa-heart " @click="likeusers"></i>
									</VueStar>
              <span class="voted_count text_en">{{like_users.length }}</span>
            </button>
				</span>
				<span class="atc_vote">
						<button class="bt_vote vote_area" type="button">
							<VueStar animate="animate__animated animate__zoomIn" color="#F05654" :check="funny_users | checkChecked(login_user.id)" >
								<i slot="icon" class="far fa-grin-hearts" ref="funnyusers"  @click="funnyusers"></i>
							</VueStar>
              <span class="voted_count text_en">{{funny_users.length }}</span>
						</button>

				</span>
				<span class="atc_vote">
						<button class="bt_vote vote_area" type="button">
							<VueStar animate="animate__animated animate__rotateIn" color="#F05654" :check="helpful_users | checkChecked(login_user.id)" >
									<i slot="icon" class="fas fa-award" @click="helpfulusers"></i>
									{{helpful_users}}
							</VueStar>
						<span class="voted_count text_en">{{helpful_users.length }}</span></button>
				</span>
			</div>

			<!-- 추천 누른 사람 목록 -->
			<div id="voted_who">
				<div class="atc_who bg_grey1 scroll_wrap show">
					<h3>이 영화를 같이 좋아해준 사람들 <span class="text_en pt_col">{{ movie_like_users.length }}</span></h3>
					<div class="scroll-wrapper inner scrollbar-macosx" style="position: relative;"><div class="inner scrollbar-macosx scroll-content scroll-scrolly_visible" style="height: auto; margin-bottom: 0px; margin-right: 0px; max-height: 105px;">
						<ul class="scroll_x">
							<li v-for="(user, idx) in movie_like_users" :key="idx">
								<span class="inkpf color round">
									<Gravatar :email="user.email" class="profile-img inkpf_img"/>
								</span>
								<br>
								<span class="vote_nickname">{{ user.username }}</span>
							</li>
							
						</ul>
					</div><div class="scroll-element scroll-x scroll-scrolly_visible"><div class="scroll-element_outer"><div class="scroll-element_size"></div><div class="scroll-element_track"></div><div class="scroll-bar" style="width: 89px;"></div></div></div><div class="scroll-element scroll-y scroll-scrolly_visible"><div class="scroll-element_outer"><div class="scroll-element_size"></div><div class="scroll-element_track"></div><div class="scroll-bar" style="height: 16px; top: 84.6743px;"></div></div></div></div>
				</div>		
			</div>

		</div>

		<!--댓글부분  -->
		<div id="comment" class="cmt cmt_bubble">
			<div class="cmt_wrap has_top">
				<!-- 댓글리스트 -->
				<div class="cmt_list">
          <CommentListItem 
            v-for="(comment, idx) in comments"
            :key ="idx"
            :comment="comment"
						:loginUser ="login_user"
						@deleteComment="updateComment"
            />
			</div>
			</div>

			<!-- 댓글 작성부분 -->
			<div class="cmt_write cmt_write_unit" v-if ="token">
				<span class="inkpf round"><Gravatar :email="useremail" class="profile-img inkpf_img"/></span>
				<form v-on:submit.prevent="commentCreate" action="/" method="post" class="cmt_form" onsubmit="" editor_sequence="65603779">
					<input type="hidden" name="error_return_url" value="/movietalk/65603779?category=376">
					<input type="hidden" name="act" value="dispBoardContent">
					<input type="hidden" name="mid" value="movietalk">
					<input type="hidden" name="document_srl" value="65603779">
					<input type="hidden" name="comment_srl" value="">
					<input type="hidden" name="content" value="">
					<div class="cmt_write_input text_ver">
						<input type="hidden" name="use_html" value="Y">
						<input type="hidden" id="htm_65603779" value="n">
						<textarea class="cmt_textarea" id="editor_65603779" cols="50" rows="4" placeholder="댓글 내용을 입력해주세요." style="width: 100%;" @keyup.enter="commentCreate" v-model="commentContent"></textarea>
					</div>
					<div class="cmt_write_option">
						<div class="bt_area bt_right">
							<button class="ib ib2 ib_color" type="submit" v-if ="token">댓글 등록</button>
						</div>
					</div>
				</form>
			</div>

			<!-- 댓글부분 끝 -->
		</div>

	</article>

	</section>
	</div>
	</div>
	</div>
	</div>
</template>

<script>
import axios from 'axios'
import Gravatar from 'vue-gravatar'
import jwt_decode from "jwt-decode";

import movieMixin from "@/mixins/movieMixin"
import CommentListItem from '@/components/CommentListItem'
import VueStar from '@/components/VueStar'
import { mapState } from 'vuex'

const BACKEND = process.env.VUE_APP_BACKEND_LINK
export default {
  name : "ReviewDetail",
	computed : {
    ...mapState([
      'token'
    ])
  },
  components : {
    CommentListItem,
		Gravatar,
    VueStar,
  },
  mixins : [movieMixin],
  data: function () {
    return {
      detail : '',
      like_users: [],
      funny_users:[],
      helpful_users: [],
      comments: [],
			commentContent: '',
			useremail:'',
			isActive:'heart-active',
			movie_like_users : [],
			login_user : "",
    }	
  },
	filters : {
		checkChecked : function(arr, id){
			console.log(arr)
			
			return arr.includes(id)
		}
	},
  methods:{
    setToken: function () {
      const config = {
        Authorization: `JWT ${this.$store.state.token}`
      }
      return config
    },
    likeusers : function () {
      axios({
        method: 'post',
        url: `${BACKEND}community/${this.$route.params.detail}/like/`,
        headers: this.setToken(),
      })
        .then(() => {
          this.getData()
        })
        .catch(err => {

          console.log(err)
        })
    },
    funnyusers : function () {
      axios({
        method: 'post',
        url: `${BACKEND}community/${this.$route.params.detail}/funny/`,
        headers: this.setToken(),
      })
        .then(() => {
					this.getData()   
        })
        .catch(err => {
          console.log(err)
        })
    },
    helpfulusers : function () {
      axios({
        method: 'post',
        url: `${BACKEND}community/${this.$route.params.detail}/helpful/`,
        headers: this.setToken(),
      })
        .then(() => {
					this.getData()
        })
        .catch(err => {
          console.log(err)
        })
    },
		commentCreate: function () {
			axios({
        method: 'post',
        url: `${BACKEND}community/${this.detail.id}/comment/`,
        headers: this.setToken(),
				data: {
					'content':this.commentContent
					}
      })
        .then(res => {
          console.log(res)
					this.$set(this.comments,0,res.data.content)
					this.getData()
					this.commentContent = ''
        })
        .catch(() => {
          alert("없는 리뷰 글입니다.")
          this.$router.push({name : 'Movies'})
        })
		},
		updateComment: function () {
			this.getData()
		},
		getData : function () {
			axios({
        method: 'get',
        url: `${BACKEND}community/${this.$route.params.detail}`,
				headers: this.setToken(),
      })
      .then(res => {
        console.log(res)
				this.movie_like_users = res.data[1]
        this.detail = res.data[0]
        this.comments = res.data[0].comment_set
        this.like_users = res.data[0].like_users
        this.funny_users = res.data[0].funny_users
        this.helpful_users = res.data[0].helpful_users
				const decoded = jwt_decode(this.$store.state.token)
		    this.useremail = decoded.email
				this.movie_like_users = res.data[1]
				this.login_user = res.data[2][0]
      })
		
		},
		loginCheck : function(){
      if (!this.$store.state.token){
        const detailItem ={
          name: 'community',
          params: this.$route.params.detail
        }
        this.$store.dispatch('setNextPage',detailItem)
        this.$router.push({name : 'Login'})
      }
    }
  },
  created: function () {
		this.loginCheck()
		this.getData()
		
    
		
  }
}
</script>

<style>
.VueStar {
	position: absolute;
	transform: translate(-48%,-30%);
}

a img
{
border:0
}
[hidden]
{
display:none
}
.rhymix_content
{
line-height:180%;
word-break:normal
}
.rhymix_content,.xe_content
{
font-family:나눔고딕,NanumGothic,Malgun Gothic,sans-serif;
font-size:13px;
word-wrap:break-word
}
.rhymix_content p,.xe_content p
{
margin:0;
line-height:180%
}
.rhymix_content p span,.xe_content,.xe_content p span
{
line-height:180%
}
.rhymix_content img,.xe_content img
{
max-width:100%;
height:auto
}
.rhymix_content ul
{
list-style-type:disc;
margin-left:1em;
margin-right:0;
padding-left:25px
}
.rhymix_content ul,.xe_content ul
{
display:block;
padding-right:0
}
.rhymix_content ul:lang(ar),.rhymix_content ul:lang(arc),.rhymix_content ul:lang(dv),.rhymix_content ul:lang(fa),.rhymix_content ul:lang(ha),.rhymix_content ul:lang(he),.rhymix_content ul:lang(khw),.rhymix_content ul:lang(ks),.rhymix_content ul:lang(ku),.rhymix_content ul:lang(ps),.rhymix_content ul:lang(ur),.rhymix_content ul:lang(yi),.xe_content ul:lang(ar),.xe_content ul:lang(arc),.xe_content ul:lang(dv),.xe_content ul:lang(fa),.xe_content ul:lang(ha),.xe_content ul:lang(he),.xe_content ul:lang(khw),.xe_content ul:lang(ks),.xe_content ul:lang(ku),.xe_content ul:lang(ps),.xe_content ul:lang(ur),.xe_content ul:lang(yi)
{
padding-left:0;
padding-right:25px;
margin-left:0;
margin-right:1em
}
.rhymix_content li,.xe_content li
{
display:list-item
}
@media screen
{
img
{
max-width:none
}

}
.xe-clearfix
{
zoom:1
}
.xe-clearfix:after,.xe-clearfix:before
{
content:" ";
display:table
}
.xe-clearfix:after
{
clear:both
}
#popup_menu_area,#rhymix_popup_menu
{
position:absolute;
z-index:9999;
margin:10px 0;
padding:0;
border:1px solid #eee;
border-radius:2px;
font-size:12px;
box-shadow:0 10px 20px rgba(0,0,0,.19),0 6px 6px rgba(0,0,0,.23);
background:#fff;
min-width:80px
}
#popup_menu_area ul,#rhymix_popup_menu ul
{
margin:0;
padding:0;
list-style:none
}
#popup_menu_area li,#rhymix_popup_menu li
{
margin:0;
padding:0;
line-height:1.5
}
#popup_menu_area a,#rhymix_popup_menu a
{
display:block;
padding:5px;
text-decoration:none;
color:#212121
}
#popup_menu_area a:active,#popup_menu_area a:focus,#popup_menu_area a:hover,#rhymix_popup_menu a:active,#rhymix_popup_menu a:focus,#rhymix_popup_menu a:hover
{
background:#eee;
outline:0
}
@media screen and (max-width:400px)
{
#popup_menu_area,#rhymix_popup_menu
{
min-width:120px;
max-width:95%;
font-size:13px
}
#popup_menu_area a,#rhymix_popup_menu a
{
display:block;
padding:10px;
text-decoration:none;
color:#212121
}

}
.rhymix_button_wrapper
{
clear:both;
margin:10px 0;
padding:0;
text-align:right;
zoom:1
}
.rhymix_button_wrapper:after
{
clear:both;
display:block;
content:""
}
.rhymix_button,.rhymix_button>a,.rhymix_button>button,.rhymix_button>input,.rhymix_button>span
{
display:inline-block;
padding:0 12px!important;
overflow:visible;
vertical-align:top;
text-decoration:none!important;
font-family:inherit;
font-size:12px;
color:#333;
cursor:pointer
}
.rhymix_button
{
margin:0;
height:24px!important;
border:1px solid #bbb;
border-color:#e6e6e6 #e6e6e6 #bfbfbf;
border-color:rgba(0,0,0,.1) rgba(0,0,0,.1) rgba(0,0,0,.25);
border-bottom-color:#a2a2a2;
border-radius:2px;
text-align:center;
text-shadow:0 1px 1px rgba(255,255,255,.75);
line-height:24px!important;
box-shadow:inset 0 1px 0 rgba(255,255,255,.2),0 1px 2px rgba(0,0,0,.05);
background-color:#f5f5f5;
background-image:-moz-linear-gradient(top,#fff,#e6e6e6);
background-image:-webkit-linear-gradient(top,#fff,#e6e6e6);
background-image:-o-linear-gradient(top,#fff,#e6e6e6);
/* background-image:linear-gradient(top,#fff,#e6e6e6); */
background-repeat:repeat-x
}
.rhymix_button:active,.rhymix_button:hover,.rhymix_button[disabled]
{
color:#333;
background-color:#e6e6e6
}
.rhymix_button>a,.rhymix_button>button,.rhymix_button>input,.rhymix_button>span
{
margin:0 -12px!important;
width:auto;
height:24px;
border:0;
line-height:24px;
background:0 0
}
button.rhymix_button,input.rhymix_button
{
height:26px!important
}
body,html
{
height:100%;
width:100%
}
body
{
margin:0;
padding:0;
-webkit-text-size-adjust:none;
font-size:14px;
-webkit-font-smoothing:subpixel-antialiased
}
a,a:active,a:hover,a:visited
{
text-decoration:none
}
a,button
{
outline:0
}
input,textarea
{
outline:0;
margin:0
}
textarea
{
resize:vertical
}
button,input[type=button]
{
cursor:pointer;
margin:0;
-webkit-font-smoothing:subpixel-antialiased!important;
border:0
}
button
{
padding:0;
background:0 0
}
h1,h2,h3,h4,h5
{
font-weight:400
}
h1,h2,h3,h4,h5,p,ul
{
padding:0;
margin:0
}
ul
{
list-style:none
}
.xe_content ul
{
list-style-type:initial;
margin:1em 0;
padding-left:40px
}
.round10
{
border-radius:10px
}
.round15
{
border-radius:15px
}
.round20
{
border-radius:20px
}
.pt_star
{
font:15px/15px verdana
}
.inkpf
{
display:inline-block;
width:40px;
height:40px;
background-size:cover;
overflow:hidden;
vertical-align:middle
}
.inkpf.round
{
border-radius:50%
}
.inkpf.small
{
width:30px;
height:30px
}
.inkpf_img
{
width:100%;
height:auto
}
.ib,.ink_header .ink_top ul
{
display:inline-block
}
.ib i
{
margin-right:3px
}
.ib i.only
{
margin-right:0;
transition-property:color;
transition-duration:.3s
}
.ib.ib_color i.only,.ib_color
{
color:#fff
}
.bt_right .ib
{
margin-left:3px;
vertical-align:middle
}
textarea:focus::-webkit-input-placeholder
{
color:#b4b1a2
}
textarea:focus::-moz-placeholder
{
color:#b4b1a2
}
textarea:focus:-ms-input-placeholder
{
color:#b4b1a2
}
textarea:focus:-moz-placeholder
{
color:#b4b1a2
}
.ink_wrap
{
position:relative;
min-height:100%;
box-sizing:border-box
}
.board_name,.board_name2
{
white-space:nowrap
}
.board_name .inner,.board_name2 .inner
{
display:inline-block;
border-radius:12px;
padding:0 10px;
box-sizing:border-box;
text-align:center;
transition-property:background-color,color;
transition-duration:.3s
}
.clearfix:after,.clearfix:before
{
content:" ";
display:table
}
.clearfix:after
{
clear:both
}
a,button,input[type=button]
{
transition-property:color,background-color,border-color;
transition-duration:.3s
}
.ib,button,input,textarea
{
font-size:14px
}
input[type=password]
{
font-family:Helvetica
}
.ib
{
height:42px;
line-height:42px;
padding:0 20px;
border-radius:10px;
position:relative;
overflow:hidden;
z-index:1
}
.font_n .ib
{
line-height:44px
}
.ib::before
{
content:'';
position:absolute;
left:0;
top:100%;
width:100%;
height:100%;
border-radius:50%;
transition-property:top,border-radius;
transition-duration:.5s;
z-index:-1
}
.ib:hover::before
{
top:50%
}
.ib2
{
height:32px;
line-height:32px;
padding:0 11px;
border-radius:5px;
font-size:13px
}
.font_n .ib2
{
line-height:33px
}
.ink_wrap .xe_content
{
font-family:NanumGothic,'apple sd gothic neo',sans-serif
}
.ink_bubble_wrap
{
position:relative;
display:inline-block
}
.ink_bubble:not(.bubble_left)
{
left:50%;
top:-35px;
transform:translateX(-50%);
transition-property:top,opacity
}
.ink_bubble
{
position:absolute;
width:0;
height:0;
overflow:hidden;
background-color:#222;
border-radius:5px;
white-space:nowrap;
font-size:11px!important;
line-height:100%!important;
font-weight:400!important;
color:#fff;
opacity:0;
transition-duration:.3s;
z-index:1
}
.has_bubble:hover+.ink_bubble:not(.bubble_left)
{
top:-25px;
opacity:1;
width:auto;
height:auto;
padding:6px 6px 4px;
overflow:visible
}
.ink_bubble::after
{
content:'';
position:absolute;
left:50%;
top:100%;
margin-left:-4px;
border:5px solid transparent;
border-top:5px solid #222
}
.ink_wrap
{
padding-bottom:200px
}
.ink_container
{
width:100%;
margin:0 auto;
border-top:1px solid transparent
}
.ink_header
{
margin-bottom:25px
}
.ink_wrapper
{
position:relative;
padding-bottom:25px
}
.ink_content
{
margin: 0 auto;
width:90%;
}
.ink_bt_top,.ink_top
{
height:40px;
line-height:40px
}
.ink_bt_top
{
display:none;
position:fixed;
right:25px;
bottom:25px;
width:40px;
border-radius:20px;
z-index:99
}
.ink_top
{
padding:0 15px;
font-size:13px;
letter-spacing:0
}
.ink_top:empty
{
display:none
}
.ink_top ul
{
display:inline-block;
vertical-align:middle
}
.ink_top li
{
display:inline-block;
margin-right:15px
}
.ink_top a
{
display:inline!important;
border-bottom:1px solid transparent
}
.ink_top .top_menu
{
float:right;
text-align:right
}
.ink_header .ink_top .top_menu
{
float:none;
margin-right:5px
}
.ink_header .ink_top
{
position:absolute;
right:0;
top:50%;
width:70%;
transform:translateY(-50%);
text-align:right;
z-index:99
}
.ink_header .ink_top li,.ink_top .top_menu li
{
margin-left:15px;
margin-right:0
}
.ink_header
{
position:relative
}
.ink_top:empty+.ink_header
{
margin-top:25px
}
.board_name .inner,.board_name2 .inner
{
font-size:12px;
height:24px;
line-height:24px;
z-index:1
}
.font_n .board_name .inner,.font_n .board_name2 .inner
{
line-height:25px
}
.board_name .inner:hover,.board_name .inner:hover a
{
color:#fff
}
.scroll-wrapper
{
overflow:hidden!important;
padding:0!important;
position:relative
}
.scroll-wrapper>.scroll-content
{
border:0!important;
box-sizing:content-box!important;
height:auto;
left:0;
margin:0;
max-height:none;
max-width:none!important;
overflow:scroll!important;
padding:0;
position:relative!important;
top:0;
width:auto!important
}
.scroll-wrapper>.scroll-content::-webkit-scrollbar
{
height:0;
width:0
}
.scroll-element
{
display:none
}
.scroll-element,.scroll-element div
{
box-sizing:content-box
}
.scroll-element.scroll-y.scroll-scrolly_visible
{
display:block
}
.scroll-element .scroll-bar
{
cursor:default
}
.scrollbar-macosx
{
height:100%
}
.scrollbar-macosx>.scroll-element,.scrollbar-macosx>.scroll-element div
{
background:0 0;
border:0;
margin:0;
padding:0;
position:absolute;
z-index:10
}
.scrollbar-macosx>.scroll-element div
{
display:block;
height:100%;
left:0;
top:0;
width:100%
}
.atc_who h3,.scrollbar-macosx>.scroll-element .scroll-element_track
{
display:none
}
.scrollbar-macosx>.scroll-element .scroll-bar
{
display:block;
opacity:0;
-webkit-border-radius:5px;
-moz-border-radius:5px;
border-radius:5px;
-webkit-transition:opacity .2s linear;
-moz-transition:opacity .2s linear;
-o-transition:opacity .2s linear;
-ms-transition:opacity .2s linear;
transition:opacity .2s linear
}
.scrollbar-macosx:hover>.scroll-element .scroll-bar
{
opacity:.7
}
.scrollbar-macosx>.scroll-element.scroll-x
{
bottom:0;
height:0;
left:0;
min-width:100%;
overflow:visible;
width:100%
}
.scrollbar-macosx>.scroll-element.scroll-y
{
height:100%;
min-height:100%;
right:0;
top:0;
width:0
}
.scrollbar-macosx>.scroll-element.scroll-x .scroll-bar
{
height:5px;
min-width:10px;
top:-5px
}
.scrollbar-macosx>.scroll-element.scroll-y .scroll-bar
{
left:-5px;
min-height:10px;
width:5px
}
.scrollbar-macosx>.scroll-element.scroll-x .scroll-element_outer
{
left:2px
}
.scrollbar-macosx>.scroll-element.scroll-x .scroll-element_size
{
left:-4px
}
.scrollbar-macosx>.scroll-element.scroll-y .scroll-element_outer
{
top:2px
}
.scrollbar-macosx>.scroll-element.scroll-y .scroll-element_size
{
top:-4px
}
.scrollbar-macosx>.scroll-element.scroll-x.scroll-scrolly_visible .scroll-element_size
{
left:-11px
}
.ink_board,.list_wrap .list_unit
{
position:relative
}
.category_color
{
display:inline-block;
width:10px;
height:10px;
border-radius:3px;
margin-right:2px
}
.list_icon
{
display:inline-block;
width:16px;
height:16px;
border-radius:5px;
text-align:center
}
.ink_atc
{
position:relative
}
.ink_atc.has_list
{
margin-bottom:15px
}
.atc_header,.atc_who li,.xe_content
{
word-break:break-all
}
.atc_header .category_color
{
width:12px;
height:12px;
border-radius:3px
}
.atc_vote button
{
display:inline-block;
height:36px;
line-height:36px;
padding:0 15px;
border-radius:10px
}
.atc_vote .bt_vote,.cmt_member_only i
{
margin-right:5px
}
.atc_vote .voted_count
{
display:inline-block;
padding-left:15px;
margin-left:15px;
transition-property:border-color;
transition-duration:.3s
}
.atc_who,.cmt_member_only
{
text-align:center
}
.atc_who.show h3
{
margin:0;
display:block;
padding:10px 0;
border-bottom:1px solid #eee
}
.atc_who li
{
display:inline-block;
width:55px;
margin:0 3px 10px;
vertical-align:top
}
.atc_who .vote_nickname
{
display:inline-block;
margin-top:3px
}
.atc_buttons_etc .ink_bubble_wrap
{
display:inline-block;
margin-left:5px
}
.atc_buttons_etc .ib
{
display:inline-block;
width:36px;
height:36px;
line-height:36px;
padding:0;
overflow:visible
}
.atc_buttons_etc .bt_report
{
position:relative
}
.atc_share .share_list
{
margin-bottom:15px
}
.atc_share .share_list>a
{
display:inline-block;
width:40px;
height:40px;
border-radius:7px;
overflow:hidden;
margin:0 5px 10px
}
.atc_share .share_list img
{
width:40px;
height:40px
}
.cmt_member_only
{
padding:50px 0
}
.cmt_member_only p
{
padding:12px 15px;
margin-bottom:15px;
border-radius:20px
}
.cmt_member_only a
{
margin:0 5px
}
.cmt_buttons,.cmt_title,.cmt_unit
{
position:relative
}
.cmt_member_only p,.cmt_title h3,.list_category2>ul
{
display:inline-block
}
.cmt_title .bt_cmt_write
{
position:absolute;
top:12px
}
.cmt_title .bt_cmt_write button
{
padding:5px 10px
}
.cmt_unit .cmt_rank
{
display:inline-block;
position:relative;
margin-right:3px;
border-radius:5px;
color:#fff;
vertical-align:bottom
}
.cmt_unit .cmt_rank i
{
position:absolute;
left:5px;
top:1px;
font-size:14px
}
.cmt_unit .cmt_rank1
{
background-color:#d4af37
}
.cmt_unit .cmt_rank2
{
background-color:#a9a9a9
}
.cmt_unit .cmt_rank3
{
background-color:#b08d55
}
.cmt_unit .nickname
{
font-weight:700
}
.cmt_buttons
{
height:24px;
margin-top:10px
}
.cmt_buttons:empty
{
display:none
}
.cmt_buttons .bt_wrap
{
display:inline-block;
border-radius:5px;
vertical-align:middle
}
.cmt_buttons .bt_wrap .bt
{
display:inline-block;
margin-right:1px;
padding:0 8px;
line-height:24px
}
.cmt_buttons .bt_wrap .bt:first-of-type
{
border-top-left-radius:5px;
border-bottom-left-radius:5px
}
.cmt_buttons .bt_wrap .bt:last-of-type
{
margin-right:0;
border-top-right-radius:5px;
border-bottom-right-radius:5px
}
.cmt_buttons .bt_cmt_report
{
margin-right:2px
}
.cmt_bubble .cmt_unit:first-of-type
{
margin-top:0
}
.cmt_bubble .inkpf_wrap
{
position:absolute;
left:0;
top:0;
text-align:center
}
.cmt_bubble .cmt_unit:not(.no_profile) .cmt_rank
{
position:absolute;
left:-5px;
top:-5px;
margin-right:0;
padding:0;
width:22px;
height:22px;
line-height:22px;
border-radius:50%
}
.cmt_bubble .cmt_header
{
padding-bottom:5px
}
.cmt_bubble .cmt_body
{
position:relative;
display:inline-block;
box-sizing:border-box;
vertical-align:bottom
}
.cmt_bubble .cmt_date_wrap
{
position:absolute;
left:100%;
bottom:0;
margin-left:5px;
vertical-align:bottom;
white-space:nowrap
}
.cmt_bubble .cmt_date_wrap .cmt_time
{
opacity:0;
transition-property:opacity;
transition-duration:.3s
}
.cmt_bubble .cmt_body:hover .cmt_date_wrap .cmt_time
{
opacity:1
}
.cmt_bubble .cmt_buttons .bt
{
background-color:#fff
}
.cmt_bubble .cmt_buttons .bt2
{
display:inline-block;
padding:0 8px;
margin-right:3px;
line-height:24px;
vertical-align:middle
}
.cmt_write_unit
{
position:relative
}
.cmt_write_unit .inkpf
{
position:absolute;
left:0
}
.cmt_write_input textarea
{
width:100%;
box-sizing:border-box;
border:0;
transition-property:background-color;
transition-duration:.3s;
overflow:hidden;
resize:none;
padding:15px;
border-radius:15px
}
.cmt_write_input textarea:focus
{
background-color:#fcf8e3
}
.cmt_write_option
{
position:relative;
margin-top:5px
}
.cmt_write_option .unit
{
margin-right:10px
}
.cmt_write_option .bt_write_type i
{
transition-property:color;
transition-duration:.3s
}
.cmt_write_option .bt_area
{
position:absolute;
right:0;
bottom:0
}
.star_point
{
position:absolute;
left:0;
top:0;
width:100%;
direction:rtl;
text-align:left
}
.star_point>span
{
display:inline-block;
overflow:hidden;
vertical-align:top;
cursor:pointer;
opacity:0
}
.write_header
{
position:relative
}
.write_header .bt_area2
{
position:absolute
}
.write_title
{
display:inline-block;
width:100%
}
.write_editor
{
margin-top:15px
}
.write_option_color
{
display:inline-block;
margin-right:10px
}
.bt_atc_font
{
background-color:#e5e5e5
}
.atc_font
{
display:inline-block;
position:relative;
margin-left:10px
}
.bt_atc_font
{
width:30px;
height:30px;
line-height:32px;
border-radius:15px;
font-size:12px
}
.list_header
{
margin-bottom:15px
}
.list_header:empty
{
display:none
}
.list_category
{
min-width:160px
}
.list_category>ul>li>ul
{
margin-left:10px;
padding-top:8px
}
.list_category2
{
margin-bottom:5px;
font-size:13px
}
.list_category2>ul>li
{
display:inline-block;
position:relative;
margin-right:5px;
margin-bottom:10px
}
.list_category2>ul>li>a
{
display:inline-block;
padding:7px 15px 8px;
border-radius:5px
}
.list_category2>ul>li>ul
{
display:none;
position:absolute;
top:40%;
left:0;
padding:0 15px 10px;
min-width:100%;
box-sizing:border-box;
border-radius:10px;
box-shadow:0 5px 5px rgba(0,0,0,.1);
opacity:0;
transition-property:top,opacity;
transition-duration:.5s;
z-index:10
}
.list_category2>ul>li>ul>li
{
white-space:nowrap;
padding-top:10px
}
.list_type
{
float:right
}
.list_type a
{
display:inline-block;
height:32px;
line-height:34px;
padding:0 10px
}
.list_type a:first-of-type
{
border-radius:5px 0 0 5px
}
.list_type a:last-of-type
{
border-radius:0 5px 5px 0
}
.list_buttons li,.list_wrap
{
position:relative
}
.list_buttons
{
position:absolute;
right:-40px;
top:0;
width:30px;
z-index:10
}
.list_buttons>div
{
width:30px;
text-align:center
}
.list_buttons li
{
margin-bottom:10px
}
.list_buttons .has_bubble
{
display:inline-block;
width:30px;
height:30px;
line-height:30px;
border-radius:50%
}
.font_n .list_buttons .has_bubble
{
line-height:32px
}
.category_color
{
margin-bottom:3px;
vertical-align:middle
}
.ink_list
{
border-radius:20px
}
.list_icon
{
margin:-2px 0 -2px 3px;
font:700 8px/16px Arial;
vertical-align:middle
}
.list_wrap .list_icon2
{
display:inline-block;
width:15px;
height:15px;
line-height:15px;
box-sizing:border-box;
padding:1px;
border-radius:3px;
margin-bottom:2px;
vertical-align:middle;
background-repeat:no-repeat;
background-position:center center;
background-size:13px 13px;
text-indent:-9999px
}
.list_wrap .list_unit
{
transition-property:background-color;
transition-duration:.3s
}
.list_wrap .list_cmt
{
display:inline-block;
padding:7px 15px;
border-radius:15px 15px 15px 5px;
font-size:12px
}
.font_n .list_wrap .list_cmt
{
padding-bottom:8px
}
.list_wrap .list_cmt .date
{
display:inline-block;
margin-left:10px;
font-size:12px
}
.atc_header h1
{
font-size:25px;
line-height:160%
}
.atc_header h1,.containerN .atc_header h1
{
padding:20px 25px
}
.atc_info
{
padding:0 25px;
line-height:44px;
font-size:13px
}
.atc_info>span
{
display:inline-block;
vertical-align:middle
}
.atc_nickname .inkpf
{
vertical-align:middle;
margin-right:5px
}
.atc_ctrl,.atc_date
{
margin-left:15px
}
.atc_ctrl a
{
margin-left:5px
}
.atc_ctrl,.atc_info_right
{
float:right
}
.atc_info_right>span
{
margin-left:10px
}
.atc_info_right .count_cmt
{
cursor:pointer
}
.atc_body
{
padding:25px
}
.atc_body .xe_content
{
font-size:14px;
line-height:180%;
margin:-25px;
padding:25px
}
.atc_body .xe_content div,.atc_body .xe_content p,.atc_body .xe_content span
{
line-height:180%
}
.atc_body.size12 .xe_content
{
font-size:12px
}
.atc_body.size13 .xe_content
{
font-size:13px
}
.atc_body.size14 .xe_content,.cmt_title h3
{
font-size:14px
}
.atc_body.size15 .xe_content
{
font-size:15px
}
.atc_body.size16 .xe_content
{
font-size:16px
}
.xe_content a:hover
{
border-color:transparent
}
.atc_body .xe_content>div
{
overflow:unset!important;
text-indent:0!important;
min-width:100%!important;
min-height:unset!important;
height:unset!important
}
.atc_vote
{
float:left;
margin-top:25px
}
.atc_vote .bt_vote:hover,.cmt_unit .cmt_buttons .bt_wrap .bt:hover,.cmt_unit .cmt_buttons .cmt_vote .bt_vote:hover
{
color:#fff
}
.atc_who
{
margin-top:25px;
padding:0 10px;
border-radius:20px;
font-size:11px
}
.atc_who.show
{
clear:both;
margin-top:15px
}
.atc_who .inner
{
height:105px
}
.atc_who ul
{
padding:25px 15px 10px
}
.bt_who
{
display:inline-block;
margin-left:10px;
margin-top:28px;
cursor:pointer
}
.atc_who .vote_nickname
{
line-height:160%
}
.atc_buttons_etc
{
float:right;
margin-top:25px
}
.atc_buttons_etc:empty
{
display:none
}
.atc_buttons_etc .bt
{
border-radius:10px
}
.font_n .atc_buttons_etc .ib
{
line-height:38px
}
.ink_atc .list_buttons .bt_top
{
display:none
}
.cmt_title
{
padding:15px 25px
}
.cmt_title .bt_cmt_write
{
right:15px
}
.cmt_unit .cmt_rank
{
padding:3px 5px 3px 21px;
font-size:10px
}
.cmt_body .xe_content
{
font-size:14px;
line-height:160%
}
.cmt_buttons .bt_wrap .bt
{
font-size:12px
}
.cmt_bubble .cmt_wrap
{
padding:25px 25px 0
}
.cmt_bubble .cmt_unit
{
padding-left:45px;
margin-top:25px
}
.cmt_bubble .inkpf_wrap
{
width:40px
}
.cmt_bubble .cmt_header
{
padding-left:13px;
font-size:13px
}
.cmt_bubble .cmt_body
{
min-width:249px;
max-width:calc(100% - 80px);
padding:14px 20px;
border-radius:15px
}
.cmt_bubble .cmt_body .xe_content
{
font-size:13px;
line-height:180%
}
.cmt_bubble .cmt_date_wrap
{
font-size:11px
}
.cmt_bubble .cmt_ctrl_wrap
{
display:inline-block;
position:relative;
z-index:5
}
.cmt_bubble .bt_cmt_ctrl
{
margin-left:5px;
padding:1px 5px 0;
border-radius:5px
}
.cmt_bubble .bt_cmt_ctrl:hover
{
color:#fff
}
.cmt_bubble .cmt_ctrl
{
display:none;
position:absolute;
top:100%;
left:0;
margin-top:5px;
border-radius:10px;
background-color:#fff;
box-shadow:0 0 15px rgba(0,0,0,.2);
z-index:2
}
.cmt_bubble .cmt_ctrl a
{
display:inline-block;
width:100%;
padding:10px 15px;
box-sizing:border-box;
white-space:nowrap
}
.cmt_bubble .cmt_ctrl a:first-of-type
{
border-radius:10px 10px 0 0
}
.cmt_bubble .cmt_ctrl a:last-of-type
{
border-radius:0 0 10px 10px;
border-bottom:none
}
.cmt_bubble .cmt_buttons .bt2
{
font-size:12px
}
.cmt_write_unit
{
padding:25px 0 25px 45px;
margin:0 25px
}
.cmt_write_unit .inkpf
{
top:25px
}
.cmt_write_option
{
height:32px
}
.star_point:hover>span
{
opacity:0!important
}
.star_point>span:hover,.star_point>span:hover~span
{
opacity:1!important
}
.write_header
{
padding:20px 25px
}
.write_header .bt_area2
{
right:15px;
top:50%;
transform:translateY(-50%)
}
.write_body
{
padding:25px
}
.write_option1
{
display:inline-block
}
.pt_bg,.pt_bg2
{
color:#fff!important
}
.cmt_title .bt_cmt_write button:hover,.document_title a:hover,a,body
{
color:#222
}
.board_name2 .inner,.cmt_member_only i,.ib_mono,.ib_monoC
{
color:#666
}
.cmt_buttons .bt_wrap .bt,.cmt_title .bt_cmt_write button,.font_grey1,.font_grey1 a,.ib i.only,.ib_mono3
{
color:#999
}
textarea::-webkit-input-placeholder
{
color:#bbb
}
textarea::-moz-placeholder
{
color:#bbb
}
textarea:-ms-input-placeholder
{
color:#bbb
}
textarea:-moz-placeholder
{
color:#bbb
}
.bg_grey1,.ib_mono3,.inkpf
{
background-color:#f7f7f7
}
.bg_grey2,.board_name2 .inner,.cmt_member_only p,.ib_mono,.ib_monoC,body
{
background-color:#eee
}
.cmt_write_option .bt_write_type i
{
color:#bbb
}
.cmt_bubble .cmt_body,.cmt_title,.cmt_write_input textarea
{
background-color:#f7f7f7
}
.cmt_member_only
{
border-top:1px solid #eee
}
.comment_date,.document_title a,.ink_rank .count
{
color:#999
}
.comment_content
{
background-color:#f7f7f7
}
.comment_content::after
{
border-top:5px solid #f7f7f7;
border-left:5px solid #f7f7f7
}
.ink_bt_top
{
background-color:rgba(255,255,255,.8)
}
.font_grey1 a:hover,.font_grey1 button:hover,.ib_mono2:hover i.only,.ib_mono3:hover,.ib_mono:hover i.only,.ink_top a:hover
{
color:#222
}
.ink_top,.ink_top a,.ink_top button
{
color:#666
}
.ink_top a:hover
{
border-bottom:1px solid #222
}
.ib_mono2
{
background-color:#e5e5e5
}
.ib_mono3::before
{
background-color:#f2f2f2
}
.ib_mono::before,.scrollbar-macosx>.scroll-element .scroll-bar
{
background-color:#ddd
}
.ib_mono2::before
{
background-color:#d5d5d5
}
.list_buttons .has_bubble:hover
{
color:#222
}
.cmt_bubble .cmt_ctrl a
{
color:#666
}
.cmt_bubble .bt_cmt_ctrl,.cmt_bubble .cmt_ctrl .bt i,.list_buttons .has_bubble,.list_category2 ul a
{
color:#999
}
.list_type a,.list_wrap .list_cmt
{
color:#bbb
}
.containerN .ink_atc
{
background-color:#fff
}
.containerN .ink_list
{
background-color:#f9f9f9
}
.atc_info,.cmt_bubble .cmt_ctrl a:hover,.ink_content .ink_rank h3,.list_buttons .has_bubble,.list_category2>ul>li>a,.list_category2>ul>li>ul,.list_type a
{
background-color:#f7f7f7
}
.atc_ctrl a
{
border-bottom:1px solid #f7f7f7
}
.cmt_bubble .bt_cmt_ctrl,.list_unit:hover .list_cmt,.list_wrap .inkpf,.list_wrap .list_cmt
{
background-color:#eee
}
.cmt_bubble .cmt_ctrl a,.containerN .write_header
{
border-bottom:1px solid #eee
}
.cmt_bubble .bt_cmt_ctrl:hover,.cmt_unit .cmt_buttons .bt_wrap .bt:hover
{
background-color:#999
}
.atc_ctrl a:hover
{
border-bottom-color:#222
}
.pt_col
{
color:#ec5e5e!important
}
.pt_bg
{
background-color:#ec5e5e!important
}
.board_name .inner,.inkpf.color
{
background-color:#e5e5e5
}
.pt_col2
{
color:#222!important
}
.board_name .inner,.board_name .inner a,.cmt_write_option .bt_write_type:hover i
{
color:#222
}
.pt_bg2
{
background-color:#222!important
}
.ib_color
{
background-color:#ec5e5e
}
.atc_vote .bt_vote
{
color:#123123
}
.cmt_buttons .cmt_vote .bt_vote
{
color:black;
}

.atc_vote .bt_vote
{
background-color:#fbdfdf
}
.atc_vote .bt_vote .voted_count
{
border-left:1px solid #f9d2d2
}
.xe_content a
{
color:#41bc99
}

</style>