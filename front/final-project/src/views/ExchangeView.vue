<template>
  <div>
    
    <p class="head-txt">환율 계산기</p>
    <div class="exchange-box">
      <ExchangeInfo />
      <ExchangeCalculator />
    </div>
    <br><br><br>
  </div>
</template>

<script setup>
import ExchangeInfo from '@/components/exchange/ExchangeInfo.vue';
import ExchangeCalculator from '@/components/exchange/ExchangeCalculator.vue';

</script>

<style scoped>
.head-txt {
  text-align: center;
  /* padding-right: 550px; */
  margin: 20px auto;
  font-family: 'S-CoreDream-6Bold';
  font-size: 40px;
}
.exchange-box {
  /* border: 1px solid black; */
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 20px;
  margin: auto;
}

h1 {
  font-size: 2.5rem;
  color: #333;
  font-family: 'S-CoreDream-6Bold';
  position: relative;
  margin: 2rem 0;
  text-align: center;
}

h1::after {
  content: '';
  position: absolute;
  bottom: -10px;
  left: 50%;
  transform: translateX(-50%);
  width: 100%;
  height: 3px;
  background-color: #007bff;
}


</style>