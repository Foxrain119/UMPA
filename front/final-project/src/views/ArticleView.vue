<template>
  <div>
    <h1>커뮤니티</h1>
    <div class="board-nav">
      <!-- <RouterLink :to="{ name: 'free-board' }">자유게시판</RouterLink> | -->
      <!-- <RouterLink :to="{ name: 'review-board' }">금융상품 리뷰</RouterLink> |
      <RouterLink :to="{ name: 'showcase-board' }">상품 자랑</RouterLink> -->
    </div>
    <RouterView />
  </div>
</template>

<script setup>
import { RouterLink, RouterView } from 'vue-router';
</script>

<style scoped>
.board-nav {
  margin: 20px 0;
  text-align: center;
}

.board-nav a {
  text-decoration: none;
  color: #333;
  padding: 5px 10px;
}

.board-nav a.router-link-active {
  color: #0f89ff;
  font-weight: bold;
}
</style>