<template>
  <div>
    <h1>금융 페이지</h1>
    <RouterLink to="search_products">예적금 상품 검색</RouterLink>
    <RouterView />
  </div>
</template>

<script setup>
import { RouterLink, RouterView } from 'vue-router';


</script>

<style scoped>

</style>