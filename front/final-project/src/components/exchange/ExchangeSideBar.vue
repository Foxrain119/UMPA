<template>
  <div class="info-box">
    <!-- 기본 환율 정보 -->
    <div class="basic-info-box">
      <p>미국 달러({{ america['cur_unit'] }}) : {{ america['deal_bas_r'] }}원 / 1$</p>
      <p>중국 위안({{ china['cur_unit'] }}) : {{ china['deal_bas_r'] }}원 / 1¥</p>
      <p>일본 엔({{ japan['cur_unit'] }}) : {{ japan['deal_bas_r'] }}원 / 1¥</p>
    </div>
  </div>
</template>

<script setup>
import { useFinanceStore } from '@/stores/finance';
const store = useFinanceStore()

const exchanges = store.exchanges
const america = exchanges.find(el => el['cur_unit'] === 'USD')
const china = exchanges.find(el => el['cur_unit'] === 'CNH')
const japan = exchanges.find(el => el['cur_unit'] === 'JPY(100)')

</script>

<style scoped>
.info-box {
  border: 1px solid black;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 10px;
  padding: 10px;
  width: 100px;
}
</style>