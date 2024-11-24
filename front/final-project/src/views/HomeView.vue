<template>
  <div>
    <h1>메인 페이지</h1>
    <MainInfo />

    <div class="home-article">
      <MainProduct />
    </div>
    <div class="side-bar">
      <MainSideBar />
    </div>

  </div>
  <br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br>
  <br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br>
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
.side-bar {
  /* position: fixed; */
  top: 10px; /* 초기 위치 */
  left: 0;
  width: 200px;
  /* background-color: lightgray; */
  padding: 20px;
  transition: top 10s ease; /* 부드러운 움직임 */
}
</style>