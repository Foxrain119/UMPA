<template>
  <div class="page-container">
    <div class="title-container">
      <h1>커뮤니티</h1>
    </div>
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
.page-container {
  width: 100%;
}

.title-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
  display: flex;
  justify-content: center;
}

h1 {
  font-size: 2.5rem;
  color: #333;
  font-family: 'S-CoreDream-6Bold';
  position: relative;
  margin: 2rem 0;
  text-align: center;
}

h1::after {
  content: '';
  position: absolute;
  bottom: -10px;
  left: 50%;
  transform: translateX(-50%);
  width: 100%;
  height: 3px;
  background-color: #007bff;
}

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