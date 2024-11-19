<template>
  <div>
    <h1>환율 페이지</h1>
    <div class="exchange-box">
      <ExchangeInfo />
      <ExchangeCalculator />
    </div>
  </div>
</template>

<script setup>
import ExchangeInfo from '@/components/exchange/ExchangeInfo.vue';
import ExchangeCalculator from '@/components/exchange/ExchangeCalculator.vue';

</script>

<style scoped>
.exchange-box {
  border: 1px solid black;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 10px;
  padding: 10px;

}
</style>