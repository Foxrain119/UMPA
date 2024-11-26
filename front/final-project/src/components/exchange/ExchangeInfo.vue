<template>
  <div class="info-box">
    <!-- 기본 환율 정보 -->
    <p>환율 정보</p>
    <div class="basic-info-box">
      <p>
        <img class="flag-img" src="http://127.0.0.1:8000/static/flag/US.gif" alt="US">
        미국 달러 <span class="gray-txt">{{ america['cur_unit'] }}</span> : {{ america['deal_bas_r'] }}원 / 1$
      </p>
      <p>
        <img class="flag-img" src="http://127.0.0.1:8000/static/flag/CN.gif" alt="CN">
        중국 위안 <span class="gray-txt">{{ china['cur_unit'] }}</span> : {{ china['deal_bas_r'] }}원 / 1¥
      </p>
      <p>
        <img class="flag-img" src="http://127.0.0.1:8000/static/flag/JP.gif" alt="JP">
        일본 엔 <span class="gray-txt">{{ japan['cur_unit'] }}</span> : {{ japan['deal_bas_r'] }}원 / 100¥
      </p>
    </div>

    <!-- 검색창 -->
    <div class="search-box">
      <select v-model="selection">
        <option
        v-for="country in exchanges"
        :value="country['cur_unit']"
        >
        {{ country['cur_nm'] }} ({{ country['cur_unit'] }})
      </option>
      </select>
      <br>
      <div class="search-ctr">
        <img class="flag-img" :src="`http://127.0.0.1:8000/static/flag/${selection.slice(0,2)}.gif`" :alt="`${selection.slice(0,2)}`">
        <span>{{ selectedCountry }}</span>
      </div>
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
  let mul = 1
  if (country['cur_unit'][4] === '1') {
    mul = 100
  } else {
    mul = 1
  }
  return `${country['cur_nm']} 1 : ${(country['deal_bas_r'] / mul).toFixed(2)}`
})
</script>

<style scoped>
select {
  width: 100%; /* 전체 폭으로 확장 */
  padding: 8px 12px; /* 편안한 클릭을 위한 패딩 */
  border: 1px solid #ccc; /* 테두리 설정 */
  border-radius: 4px; /* 둥근 모서리 */
  background-color: white; /* 배경색 */
  font-size: 16px; /* 글자 크기 */
  cursor: pointer; /* 커서 스타일 */
}
select:hover {
  border-color: #888; /* 호버시 테두리 색 변경 */
}
select:focus {
  border-color: #0056b3; /* 포커스시 테두리 색 변경 */
  outline: none; /* 기본 아웃라인 제거 */
}

.info-box {
  display: flex;
  flex-direction: column;
  /* justify-content: center; */
  /* align-items: center; */

  gap: 10px;
  padding: 10px;
  width: 730px;

  border-radius: 15px;
  box-shadow: 0 0 4px rgba(134, 134, 134, 0.5);
  background-color: rgb(248, 249, 250);
}

.info-box > p {
  font-family: 'S-CoreDream-6Bold';
  font-size: 25px;
  margin: 0;
  margin-left: 10px;
}

.basic-info-box {
  /* border: 1px solid black; */
  width: 700px;
  margin: 0;
}
.basic-info-box > p {
  padding: 3px 5px;
  margin: 0;

  font-size: 17px;
}

.search-box {
  /* border: 1px solid black; */
  width: 700px;
}

.flag-img {
  width: 45px;
  height: 25px;
  margin: 5px;
  margin-top: 1px;
  border-radius: 5px;
}

.search-ctr {
  padding-top: 8px;
}

.gray-txt {
  color: rgb(129, 129, 129);
}
</style>