<template>
  <div>
    <h1>금융 페이지</h1>
    <div class="txt_box">
      <RouterLink to="deposit">예적금 상품 검색</RouterLink> |
      <RouterLink to="algo1">상품 추천</RouterLink>
    </div>
    <RouterView />
  </div>
</template>

<script setup>
import { RouterLink, RouterView } from 'vue-router';


</script>

<style scoped>
/* .txt_box {
  text-align: center;
} */
</style>