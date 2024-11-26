<template>
  <div>
    <div class="txt_box">
      <RouterLink
        to="algo1"
        class="nav-link"
        :class="{ active: $route.path.includes('algo1') }"
      >
        추천 알고리즘 1
      </RouterLink> |
      <RouterLink
        to="algo2"
        class="nav-link"
        :class="{ active: $route.path.includes('algo2') }"
      >
        추천 알고리즘 2
      </RouterLink>
    </div>
    <RouterView />
  </div>
</template>

<script setup>

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