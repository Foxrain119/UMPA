<template>
  <article>
    <p>MainProduct</p>
    <div class="container">
      <p>최고 금리 상품</p>
      <span class="pdt-kind" @click.prevent="toDep">예금</span> | <span class="pdt-kind" @click.prevent="toSav">적금</span>
      <div v-show="flag">
        <div 
        class="card card-wth m-1 row"
          v-for="(product, index)  in deposits"
          :key="index"
          @click.prevent="goDetail(product)"
        >
          <div class="card-detail">
          <p style="margin-right: 10px;">{{ index + 1 }}</p>
          <p class="pdt-name">{{ product.fin_prdt_nm }}</p>
          <p class="pdt-bank">{{ product.kor_co_nm }}</p>
          <p>{{ product.option.reduce((max, cur) => {
                return cur.intr_rate2 > max ? cur.intr_rate2 : max;
              }, product.option[0].intr_rate2) }}%</p>
          </div>
        </div>
      </div>

      <div v-show="!flag">
        <div 
        class="card card-wth m-1 row"
          v-for="(product, index) in savings"
          :key="index"
          @click.prevent="goDetail(product)"
        >
          <div class="card-detail">
          <p style="margin-right: 10px;">{{ index + 1 }}</p>
          <p class="pdt-name">{{ product.fin_prdt_nm }}</p>
          <p class="pdt-bank">{{ product.kor_co_nm }}</p>
          <p>{{ product.option.reduce((max, cur) => {
                return cur.intr_rate2 > max ? cur.intr_rate2 : max;
              }, product.option[0].intr_rate2) }}%</p>
          </div>
        </div>
      </div>
    </div>
  </article>
</template>




<script setup>
import { ref } from 'vue'
import { useFinanceStore } from '@/stores/finance';

const store = useFinanceStore()
const count = 5
const deposits = store.deposits.slice(0,5)
const savings = store.savings.slice(0,5)
const flag = ref(true)

const goDetail = (product) => {
  store.goDetail(product)
}

const toDep = () => {
  flag.value = true
}
const toSav = () => {
  flag.value = false
}
</script>





<style scoped>
article {
  border: 1px solid black;
  width: 500px;
  margin: auto;
}
.card-wth {
  cursor: pointer;
  width: 420px;
}
.card-detail {
  display: flex;
  align-items: center;
}
.card-detail > p {
  margin: 0;
}
.pdt-kind {
  cursor: pointer;
}
.pdt-name {
  width: 160px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.pdt-bank {
  width: 160px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
</style>