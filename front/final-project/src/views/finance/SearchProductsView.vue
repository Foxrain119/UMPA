<template>
  <div>
    <div class="txt_box">
      <RouterLink 
        to="/deposit"
        class="nav-link"
        :class="{ active: $route.path.includes('deposit') }"
      >예금</RouterLink> |
      <RouterLink 
        to="/saving"
        class="nav-link"
        :class="{ active: $route.path.includes('saving') }"
      >적금</RouterLink>
    </div>
    <RouterView />
  </div>
</template>

<script setup>
import { RouterLink, RouterView } from 'vue-router';
</script>

<style scoped>
.txt_box {
  text-align: center;
  margin-bottom: 2rem;
  display: flex;
  justify-content: center;
  gap: 1rem;
  align-items: center;
}

.nav-link {
  padding: 0.5rem 1rem;
  color: #666;
  text-decoration: none;
  transition: color 0.3s ease;
}

.nav-link.active {
  color: #007bff;
  font-weight: bold;
}
</style>