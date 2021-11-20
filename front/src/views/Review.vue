<template>
<div class="background">
  <ReviewDetail />
</div>
</template>

<script>
import ReviewDetail from '@/components/ReviewDetail'
export default {
  name: 'Review',
  components : {
    ReviewDetail,
  },

}
</script>

<style >
/* .background {

  background: #262626;
} */
.ReviewText{
  font-size: 24px;
  font-weight: 300;
} 


</style>