<template>
  <div>
    <RouterLink :to="{ name: 'deposit' }">예금</RouterLink> |
    <RouterLink :to="{ name: 'saving' }">적금</RouterLink>
    <RouterView />
  </div>
</template>

<script setup>
import { RouterLink, RouterView } from 'vue-router';
import { onMounted } from 'vue';
import { useFinanceStore } from '@/stores/finance';

const store = useFinanceStore()

onMounted(() => {
  store.getDeposits()
})
</script>

<style scoped>

</style>