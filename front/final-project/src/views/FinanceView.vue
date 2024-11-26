<template>
  <div class="finance-container">
    <div class="title-container">
      <h1>금융 상품 비교</h1>
    </div>
    <div class="menu-container">
      <div class="nav-links">
        <div>
          <RouterLink 
            to="search_products" 
            class="nav-link"
            :class="{ 'router-link-active': $route.path.includes('deposit') || $route.path.includes('saving') }"
          >
            예적금 상품 검색
          </RouterLink>
        </div>
        <span class="divider">|</span>
        <div>
          <RouterLink to="recommend_products" class="nav-link">맞춤형 상품 추천</RouterLink>
        </div>
      </div>
    </div>
    <RouterView />
  </div>
</template>

<script setup>
import { RouterLink, RouterView } from 'vue-router';
</script>

<style scoped>
.finance-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.title-container {
  display: flex;
  justify-content: center;
  margin-bottom: 2rem;
}

h1 {
  font-size: 2.5rem;
  color: #333;
  font-family: 'S-CoreDream-6Bold';
  position: relative;
  text-align: center;
}

/* h1::after {
  content: '';
  position: absolute;
  bottom: -10px;
  left: 50%;
  transform: translateX(-50%);
  width: 100%;
  height: 3px;
  background-color: #007bff;
} */

.menu-container {
  display: flex;
  justify-content: center;
  width: 100%;
  margin-bottom: 2rem;
}

.nav-links {
  display: inline-flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
}

.nav-link {
  color: #666;
  text-decoration: none;
  transition: all 0.3s ease;
}

.divider {
  color: #666;
  font-size: 1.1rem;
}

.nav-link:hover {
  color: #007bff;
}

.router-link-active {
  color: #007bff;
  font-weight: bold;
}
</style>