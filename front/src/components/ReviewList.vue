<template>
<div class="container">
  <div class="row">
    <ReviewListItem 
      v-for="(review, idx) in reviews"
      :key ="idx"
      :review="review"
      class="col d-flex"
    />
  </div>
</div>

</template>

<script>
import ReviewListItem from'@/components/ReviewListItem'

export default {
  name: 'ReviewList',
  components : {
    ReviewListItem
  },
  props : {
    reviews : {
      type: Array,
    }
  }
  
  
}
</script>

<style scoped>
/* * {
  background: #262626;
  
} */
</style>