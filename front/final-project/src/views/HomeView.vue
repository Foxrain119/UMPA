<template>
  <div>
    <MainInfo />

    <div class="home-article">
      <MainProduct />
    </div>
    <div class="bottom-banner">
      <MainSideBar />
    </div>

  </div>
  <br><br>
</template>

<script setup>
import MainInfo from '@/components/MainInfo.vue';
import MainProduct from '@/components/MainProduct.vue';
import MainSideBar from '@/components/MainSideBar.vue';

import { useFinanceStore } from '@/stores/finance';
import { ref, computed } from 'vue';

const store = useFinanceStore()

const scrollY = ref(0)  // 현재 스크롤 위치
const triggerPoint= ref(150)  // sticky 동작을 시작할 위치

// onscroll() {

// }

const computedTop = computed(() => {
  return scrollY.value
})
</script>

<style scoped>
.home-body {
  /* display: flex; */
}
.home-article {
  /* wi */
}
.bottom-banner {

}
</style>