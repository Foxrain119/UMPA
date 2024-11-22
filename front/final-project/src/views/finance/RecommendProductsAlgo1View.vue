<template>
  <div class="search-box">
    <form class="search-condition">
      <div>{{ username }}님과 비슷한 유저의 인기 가입 상품</div>

      <div>
        <label for="merital_status">결혼 여부 :</label>
        <select name="merital_status" id="merital_status" v-model="merital_status">
          <option :value="null">전체</option>
          <option :value="false">미혼</option>
          <option :value="true">기혼</option>
        </select>
  
        <label for="gender">성별 :</label>
        <select name="gender" id="gender" v-model="gender">
          <option :value="null">전체</option>
          <option value="M">남성</option>
          <option value="F">여성</option>
        </select>
      </div>
  
      <label for="age">나이 :</label>
      <input type="number" id="age" name="age" v-model="age" min="20">

      <div v-show="age">
        <label for="age_range">나이 범위 :</label>
        <select name="age_range" id="age_range" v-model="ageRange">
          <option :value="0">동갑</option>
          <option :value="3">3세 ({{ age - 3 }}~{{ age + 3 }})</option>
          <option :value="5">5세 ({{ age - 5 }}~{{ age + 5 }})</option>
          <option :value="7">7세 ({{ age - 7 }}~{{ age + 7 }})</option>
          <option :value="10">10세 ({{ age - 10 }}~{{ age + 10 }})</option>
        </select>
      </div>

      <div>
        <label for="property">자본 :</label>
        <input type="number" id="property" name="property" v-model="property" min="0"><span></span>
        <label for="property_range">범위 :</label>
        <input type="number" id="property_range" name="property_range" v-model="propertyRange" min="1" max="50"><span>%</span>
      </div>
      
      <div>
        <input type="submit" value="추천">
      </div>
    </form>
  </div>
</template>


<script setup>
import { computed, ref } from 'vue'
import { useAccountStore } from '@/stores/account';
import { useFinanceStore } from '@/stores/finance';
import { onMounted } from 'vue';

const store2 = useAccountStore()
const store = useFinanceStore()

onMounted(() => {
  store2.getUserInfo()
})

const userInfo = store2.userInfo

const age = ref(null)
const ageRange = ref(0)
const gender = ref(null)
const property = ref(null)
const propertyRange = ref(5)
const merital_status = ref(null)

const recommendProducts = ref()

const deposits = store.deposits
const savings = store.savings



</script>


<style scoped>
.search-box {
  position: relative;
  width: 1000px;
  margin: 0 auto;
}
.search-condition {
  border: 1px solid black;
  width: 900px;
}
</style>