<template>
  <div class="VueStar"> 
    <div class="VueStar__ground">
      <div class="VueStar__icon" @click="toggle" :class="AnimateClass" :style='{color:ColorValue}'>
        <slot name="icon"></slot>
      </div>
      <div class="VueStar__decoration" :class="{ 'VueStar__decoration--active':active}"></div>
    </div>
  </div>
</template>

<script>
import { isColors } from '@/assets/vueStar/colorRE.js'
export default {
  name: 'VueStar',
  props: {
    animate: String,
    color: String,
    check : {
      type: Boolean,
      default : false
    }
  },
  methods: {
    toggle () {
      console.log("작동체크 토글")
      this.active = !this.active
      this.toggleAnimate = !this.toggleAnimate
      this.toggleColor = !this.toggleColor
    }
  },
  data () {
    return {
      active: false,
      toggleAnimate: false,
      toggleColor: false
    }
  },
  computed: {
    AnimateClass () {
      return this.toggleAnimate ? this.animate : ''
    },
    ColorValue () {
      return this.toggleColor ? this.color : ''
    }
  },
  created : function(){
    this.active = this.check
    this.toggleAnimate = this.check
    this.toggleColor = this.check
  },
  mounted () {
    if (this.color) {
      if (isColors(this.color)) {
        return
      } else {
        console.error('this color must be hexcolor or rgbcolor  ---VueStar')
      }
    } else {
      return
    }
  }
}
</script>

<style>
.VueStar{
  position: absolute;
}
.VueStar__ground {
    width: 100px;
    height: 100px;
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
  }
.VueStar__icon {
  z-index: 888; 
}
.VueStar__decoration {
  width: 100px;
  height: 100px;
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  right: 0;
  background : url("../assets/vueStar/image.png") no-repeat;
  background-position: 0 0;
  transition: background-position 1s steps(25);
  transition-duration: 0s;
}
.VueStar__decoration--active {
    transition-duration: 1s;
    background-position: -2500px 0;
  }
</style>