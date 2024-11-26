<template>
  <div class="img-container">
    <div class="main-box">
      <p class="main-text">당신의 금융, 
        <br> 
        <span class="umpa-text">UMPA</span> 와 함께 &nbsp;
        <span>  </span>
        <span class="upgrade-text">Upgrade</span> 하세요!
      </p>
      <img class="up-img" :src="mascotte" alt="mascotte">
    </div>
    
  </div>
</template>

<script setup>
import { useAccountStore } from '@/stores/account';

const store2 = useAccountStore()

const upgrade_fin = store2.images.main_page.upgrade_fin
const mascotte = store2.images.main_page.mascotte
</script>

<style scoped>
.img-container {
  height: 300px;
  /* border: 1px solid black; */
  background-color: rgb(159, 239, 255);
}
.main-box {
  width: 600px;
  position: relative;
  text-align: center;
  justify-content: center;
  margin: auto;
}
.main-text {
  position: absolute;
  top: 120px;
  left: px;

  font-family: 'Paperlogy-8ExtraBold';
  color: #000;
  font-size: 22px;
  
}
.umpa-text {
  color: white;
  text-shadow: 
    -1px -1px 1px #000,  
    1px -1px 1px #000,
    -1px 1px 1px #000,
    1px 1px 1px #000; /* 글자 테두리 */
}
.upgrade-text {
  font-size: 30px;
  /* color: rgb(156, 0, 196); */
  /* text-shadow: 
    -1px -1px 0 rgb(255, 77, 77),  
    1px -1px 0 rgb(255, 77, 77),
    -1px 1px 0 rgb(255, 77, 77),
    1px 1px 0 rgb(255, 77, 77); */
}
.up-img {
  position: absolute;
  width: 180px;
  top: 80px;
  right: 0px;
}
</style>