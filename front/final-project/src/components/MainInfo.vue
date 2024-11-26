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
  height: 500px;
  /* border: 1px solid black; */
  background-color: rgb(159, 239, 255);
  align-content: center;
}
.main-box {
  width: 1000px;
  display: flex;
  justify-content: space-between;
  margin: auto;
}
.main-text {
  /* position: absolute;
  top: 90px; */
  text-align: center;
  align-content: center;

  font-family: 'Paperlogy-8ExtraBold';
  color: #000;
  font-size: 30px;
  
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
  font-size: 45px;
  background: linear-gradient(45deg, blue, red); /* 그라데이션 적용, 방향과 색상 조정 가능 */
  -webkit-background-clip: text; /* 크롬, 사파리 등의 브라우저에 대한 설정 */
  background-clip: text; /* 텍스트 영역으로 배경 제한 */
  color: transparent; /* 글자 색상 투명으로 설정해 배경 그라데이션만 보이도록 함 */
  padding: 6px 0; /* 상단과 하단에 패딩 추가 */
}
.up-img {
  width: 280px;
  /* position: absolute; */
  /* top: 40px;
  right: 50px; */
}
</style>