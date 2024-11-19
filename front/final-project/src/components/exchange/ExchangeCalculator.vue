<template>
  <div class="cal-box">
    <p>계산기</p>
    <div class="compare-box">
      <form>
        <select name="select_from" v-model="selectedFrom">
          <option value="KRW">KRW</option>
          <option
            v-for="country in exchanges"
            :value="country['cur_unit']"
          >
            {{ country['cur_unit'] }} 
          </option>
        </select>
        <label for="money"></label>
        <input type="number" name="money" v-model="curMoney">
        <span></span>
      </form>
    </div>
    <div class="compare-box">
      <form>
        <select name="select_to" id="" v-model="selectedTo">
          <option value="KRW">KRW</option>
          <option
            v-for="country in exchanges"
            :value="country['cur_unit']"
            :selected="country['cur_unit'] === 'USD' ? true : false"
          >
            {{ country['cur_unit'] }}
          </option>
        </select>
      </form>
      <p>{{ exchangedMoney }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useFinanceStore } from '@/stores/finance';

const store = useFinanceStore()

const exchanges = store.exchanges

const selectedFrom = ref('KRW')
const selectedTo = ref('USD')

const curMoney = ref(1000)
const exchangedMoney = computed(() => {
  const exchangeTo = exchanges.find((el) => el['cur_unit'] === selectedTo.value)
  
  let cur = 0
  if (selectedFrom.value === 'KRW'){
    cur = curMoney.value 
  } else {    
    cur = curMoney.value * exchanges.find((el) => el['cur_unit'] === selectedFrom.value)['deal_bas_r']
  }

  let after = cur
  if (selectedTo.value === 'KRW'){
    if (selectedFrom.value ==='KRW');
    else after = (curMoney.value * exchanges.find((el) => el['cur_unit'] === selectedFrom.value)['deal_bas_r']).toFixed(2);
  } else {
    after = (cur / exchanges.find((el) => el['cur_unit'] === selectedTo.value)['deal_bas_r']).toFixed(2);
  }
  return after
})
</script>


<style scoped>
.cal-box {
  border: 1px solid black;
  width: 730px;
}
.compare-box {
  border: 1px solid black;
  height: 200px;
  margin: 10px;
}
</style>