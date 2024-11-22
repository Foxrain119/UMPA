<template>
  <div>
    <h1>메인 페이지</h1>
    <MainInfo />
    <div>
      <MainProduct />
      <MainSideBar />
    </div>
  </div>
</template>

<script setup>
import MainInfo from '@/components/MainInfo.vue';
import MainProduct from '@/components/MainProduct.vue';
import MainSideBar from '@/components/MainSideBar.vue';
import { useFinanceStore } from '@/stores/finance';

const store = useFinanceStore()
</script>

<style scoped>

</style>