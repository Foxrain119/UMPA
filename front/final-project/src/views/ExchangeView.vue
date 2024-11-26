<template>
  <div class="page-container">
    <div class="title-container">
      <h1>환율 계산기</h1>
    </div>
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
.page-container {
  width: 100%;
}

.title-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
  display: flex;
  justify-content: center;
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

.exchange-box {
  max-width: 1200px;
  width: 100%;
  margin: 0 auto;
  padding: 2rem;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
</style>