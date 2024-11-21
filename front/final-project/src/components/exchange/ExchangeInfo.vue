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
  border: 1px solid black;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 10px;
  padding: 10px;
  width: 730px;
}
.basic-info-box {
  border: 1px solid black;
  width: 700px;
}
.search-box {
  border: 1px solid black;
  width: 700px;
}
.info-box > p {
  margin: 10px 5px;

}
</style>