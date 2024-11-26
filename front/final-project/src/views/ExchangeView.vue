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
  gap: 10px;
  padding: 10px;

}
</style>