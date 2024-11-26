<template>
  <div class="cal-box">
    <!-- <p>환율 계산</p> -->
    <div class="compare-box">

      <form>
        <p>환전할 금액</p>
        <div>
          <select name="select_from" v-model="selectedFrom">
            <option value="KRW 한국 원">KRW 한국 원</option>
            <option
              v-for="country in exchanges"
              :value="country['cur_unit']"
            >
            {{ country['cur_unit'] }} {{ country['cur_nm'] }}
            </option>
          </select>
        </div>
        <div>
          <label for="money"></label>
          <input type="number" name="money" id="money" v-model="curMoney">
          <span></span>
        </div>
      </form>
    </div>

    <button class="chg-btn" @click.prevent="switchCountry">↕</button>

    <div class="compare-box">
      <form>
        <p>계산된 금액</p>
        <select name="select_to" id="" v-model="selectedTo">
          <option value="KRW 한국 원">KRW 한국 원</option>
          <option
            v-for="country in exchanges"
            :value="country['cur_unit']"
            :selected="country['cur_unit'] === 'USD' ? true : false"
          >
          {{ country['cur_unit'] }} {{ country['cur_nm'] }}
        </option>
        </select>
      </form>
      <p class="answer">{{ exchangedMoney }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useFinanceStore } from '@/stores/finance';

const store = useFinanceStore()

const exchanges = store.exchanges

const selectedFrom = ref('KRW 한국 원')
const selectedTo = ref('USD')

const curMoney = ref(1000)
const exchangedMoney = computed(() => {
  
  let cur = 0
  if (selectedFrom.value === 'KRW 한국 원'){
    cur = curMoney.value 
  } else {    
    cur = curMoney.value * exchanges.find((el) => el['cur_unit'] === selectedFrom.value)['deal_bas_r']
  }

  let after = cur
  if (selectedTo.value === 'KRW 한국 원'){
    if (selectedFrom.value ==='KRW 한국 원');
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
select {
  width: 620px; /* 전체 폭으로 확장 */
  padding: 8px 12px; /* 편안한 클릭을 위한 패딩 */
  margin: auto;
  margin-bottom: 10px;
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

form > div {
  text-align: center;
}

form > p {
  margin: 7px 0 2px 5px;
  /* margin-left: 37px; */
}

.cal-box {
  display: flex;
  flex-direction: column;
  align-items: center;
  
  padding: 10px;
  width: 730px;

  border-radius: 15px;
  box-shadow: 0 0 4px rgba(134, 134, 134, 0.5);
  background-color: rgb(248, 249, 250);
}
.cal-box > p {
  margin: 0;
}

.chg-btn {
  border-style: none;
  width: 60px;
  border-radius: 10px;
  background-color: white;
  box-shadow: 0 0 4px rgba(134, 134, 134, 0.5);
  font-size: 20px;
  padding: 10px 0;
}

.compare-box {
  /* border: 1px solid black; */
  min-height: 100px;
  margin: 10px;
}

input[type="number"]::-webkit-inner-spin-button,
input[type="number"]::-webkit-outer-spin-button {
  -webkit-appearance: none;
  margin: 0;
}
input[type="number"] {
  -moz-appearance: textfield;
}
input[type="number"], .answer {
  border: none; /* 테두리 제거 */
  /* 추가 스타일링 */
  padding: 8px;
  width: 100%;
  text-align: center;
  background-color: rgb(248, 249, 250);

  font-family: 'Freesentation-7Bold';
  font-size: 45px;
}
</style>