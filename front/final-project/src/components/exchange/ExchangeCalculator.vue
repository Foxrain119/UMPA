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
      </form>
    </div>
    <button @click.prevent="switchCountry">↕</button>
    <div class="compare-box">
      <form class="result-form">
        <select name="select_to" v-model="selectedTo">
          <option value="KRW">KRW</option>
          <option
            v-for="country in exchanges"
            :value="country['cur_unit']"
            :selected="country['cur_unit'] === 'USD' ? true : false"
          >
            {{ country['cur_unit'] }}
          </option>
        </select>
        <input type="text" :value="exchangedMoney" readonly class="result-input">
      </form>
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

const switchCountry = function () {
  const tmp = selectedFrom.value
  selectedFrom.value = selectedTo.value
  selectedTo.value = tmp

  curMoney.value = exchangedMoney['_value']
}

</script>


<style scoped>
.cal-box {
  border: none;
  border-radius: 8px;
  background-color: #f8f9fa;
  padding: 2rem;
  width: 100%;
}

.cal-box p {
  margin-bottom: 1.5rem;
  color: #495057;
  font-weight: bold;
  font-size: 1.1rem;
  text-align: left;
}

.compare-box {
  border: none;
  background-color: white;
  border-radius: 8px;
  padding: 1.5rem;
  margin: 1rem 0;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
  height: auto;
}

form {
  display: flex;
  gap: 1rem;
  align-items: center;
}

select {
  width: 200px;
  padding: 0.8rem;
  border: 1px solid #ced4da;
  border-radius: 4px;
  font-size: 1rem;
  color: #495057;
}

input[type="number"] {
  flex: 1;
  padding: 0.8rem;
  border: 1px solid #ced4da;
  border-radius: 4px;
  font-size: 1rem;
  color: #495057;
}

button {
  display: block;
  width: 50px;
  height: 50px;
  margin: 1rem auto;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 25px;
  font-size: 1.5rem;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

button:hover {
  background-color: #0056b3;
}

p {
  margin: 0;
  font-size: 1.2rem;
  color: #495057;
  text-align: right;
}

.result-form {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.result-input {
  flex: 1;
  padding: 0.8rem;
  border: 1px solid #ced4da;
  border-radius: 4px;
  font-size: 1rem;
  color: #495057;
  background-color: #f8f9fa;
  text-align: left;
}

/* 반응형 디자인 */
@media (max-width: 768px) {
  form, .result-form {
    flex-direction: column;
  }

  select, .result-input {
    width: 100%;
  }
}
</style>