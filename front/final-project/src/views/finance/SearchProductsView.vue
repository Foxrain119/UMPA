<template>
  <div>
    <div class="txt_box">
      <RouterLink 
        :to="{ name: 'deposit' }"
        class="router-link-active router-link-exact-active"
        aria-current="page"
      >예금</RouterLink> |
      <RouterLink :to="{ name: 'saving' }">적금</RouterLink>
    </div>
    <RouterView />
    <br><br><br><br><br>
  </div>
</template>

<script setup>
import { RouterLink, RouterView } from 'vue-router';

</script>

<style scoped>
.txt_box {
  text-align: center;
}
</style>