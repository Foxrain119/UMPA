<template>
  <div class="finance-container">
    <h1>금융 상품 비교</h1>
    <div class="nav-links">
      <RouterLink 
        to="search_products" 
        class="nav-link"
        :class="{ 'router-link-active': $route.path.includes('deposit') || $route.path.includes('saving') }"
      >
        예적금 상품 검색
      </RouterLink>
      <RouterLink to="algo1" class="nav-link">상품 추천</RouterLink>
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

h1 {
  color: #333;
  margin-bottom: 2rem;
  text-align: center;
}

.nav-links {
  display: flex;
  justify-content: center;
  gap: 2rem;
  margin-bottom: 2rem;
}

.nav-link {
  padding: 0.5rem 1rem;
  color: #666;
  text-decoration: none;
  border-radius: 4px;
  transition: all 0.3s ease;
}

.nav-link:hover {
  color: #007bff;
  background-color: #f8f9fa;
}

.router-link-active {
  color: #007bff;
  font-weight: bold;
}
</style>