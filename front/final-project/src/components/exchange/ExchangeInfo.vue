<template>
  <div class="info-box">
    <!-- 기본 환율 정보 -->
    <div class="basic-info-box">
      <p>미국 달러({{ america['cur_unit'] }}) : {{ america['deal_bas_r'] }}원 / 1$</p>
      <p>중국 위안({{ china['cur_unit'] }}) : {{ china['deal_bas_r'] }}원 / 1¥</p>
      <p>일본 엔({{ japan['cur_unit'] }}) : {{ japan['deal_bas_r'] }}원 / 1¥</p>
    </div>
    <!-- 검색창 -->
    <div class="search-box">
      <p>검색창</p>
      <select v-model="selection">
        <option
            v-for="country in exchanges"
            :value="country['cur_unit']"
          >{{ country['cur_nm'] }} ({{ country['cur_unit'] }})
          </option>
      </select>
      <span>{{ selectedCountry }}</span>
    </div>
  </div>
</template>

<script setup>
import { computed, ref} from 'vue'
import { useFinanceStore } from '@/stores/finance';

const store = useFinanceStore()
const exchanges = store.exchanges
const america = store.exchanges.find(el => el['cur_unit'] === 'USD')
const china = store.exchanges.find(el => el['cur_unit'] === 'CNH')
const japan = store.exchanges.find(el => el['cur_unit'] === 'JPY(100)')

const selection = ref('AUD')
const selectedCountry = computed(() => {
  const country = store.exchanges.find(el => el['cur_unit'] === selection.value)
  return `${country['cur_nm']} : ${country['deal_bas_r']}`
})
</script>

<style scoped>
.info-box {
  border: none;
  border-radius: 8px;
  background-color: #f8f9fa;
  padding: 2rem;
  margin-bottom: 2rem;
  width: 100%;
}

.basic-info-box {
  border: none;
  background-color: white;
  border-radius: 8px;
  padding: 1.5rem;
  margin-bottom: 1.5rem;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
  width: 100%;
}

.basic-info-box p {
  margin: 0.8rem 0;
  color: #495057;
  font-size: 1.1rem;
}

.search-box {
  border: none;
  background-color: white;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
  width: 100%;
}

.search-box p {
  margin-bottom: 1rem;
  color: #495057;
  font-weight: bold;
}

select {
  width: 100%;
  padding: 0.8rem;
  border: 1px solid #ced4da;
  border-radius: 4px;
  margin-bottom: 1rem;
  font-size: 1rem;
  color: #495057;
}

span {
  display: block;
  padding: 0.8rem;
  background-color: #f8f9fa;
  border-radius: 4px;
  color: #495057;
  font-size: 1.1rem;
}
</style>