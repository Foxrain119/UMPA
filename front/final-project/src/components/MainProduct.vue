<template>
  <article>
    <!-- 검색 -->
    <div class="container content">
      <div class="info-box">
        <p class="title">Seaching Financial Products</p>
        <p class="title2">예적금 상품 검색 기능</p>
        <p class="sub-txt">당신이 찾는 상품을 검색해보세요</p>
        <p class="sub-txt">기간, 최고 한도, 금리, 키워드 등 세부적인 검색 기능이 제공됩니다</p>
        <button @click.prevent="goFinance">검색 기능 이용하기  ></button>
      </div>
      
      <div>
        <div class="content-name">
          <p>최고 금리 상품</p>
        </div>
        <div class="product-switch">
          <span class="pdt-deposit" @click.prevent="toDep">예금</span><span class="pdt-saving" @click.prevent="toSav">적금</span>
        </div>
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
    </div>

    <!-- 추천 -->
    <div class="container content even-content">
      <div class="content-name">
        <img class="recommend-img" :src="recommend" alt="recommend">
      </div>

      <div class="info-box">
        <p class="title-right">Recommend Financial Products</p>
        <p class="title2">나에게 맞는 상품 추천</p>
        <p class="sub-txt">당신에게 적합한 상품을 추천해드립니다</p>
        <p class="sub-txt">자신의 비슷한 유저들의 가장 많이 가입한 상품을 확인해보세요</p>
        <p class="sub-txt"></p>
        <button @click.prevent="goRecommend">추천 기능 이용하기  ></button>
      </div>
    </div>

    <!-- 환율 -->
    <div class="container content">
      <div class="info-box">
        <p class="title" style="color: rgb(255, 64, 64);">Exchange Information</p>
        <p class="title2">환율 정보 및 계산기</p>
        <p class="sub-txt">현재 환율 정보를 제공합니다</p>
        <p class="sub-txt">환율 계산기를 통해 예상 환전 금액을 확인해보세요</p>
        <p class="sub-txt"></p>
        <button @click.prevent="goExchange">환율 기능 이용하기  ></button>
      </div>
      
      <div class="content-name">
        <img class="recommend-img" :src="exchange" alt="exchange">
      </div>
    </div>

    <!-- 은행 -->
    <div class="container content even-content">
      <div class="content-name">
        <img class="recommend-img" :src="map" alt="map">
      </div>

      <div class="info-box">
        <p class="title">Rocation of Bank</p>
        <p class="title2">나에게 가까운 은행 찾기</p>
        <p class="sub-txt">가까운 은행을 확인하세요</p>
        <p class="sub-txt">자신이 선택한 위치의 은행 위치를 표시해줍니다</p>
        <p class="sub-txt"></p>
        <button @click.prevent="goMap">지도 기능 이용하기  ></button>
      </div>
    </div>
  </article>
</template>




<script setup>
import { ref } from 'vue'
import { useFinanceStore } from '@/stores/finance';
import { useRouter } from 'vue-router/dist/vue-router';

const router = useRouter()

const store = useFinanceStore()

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

import { useAccountStore } from '@/stores/account';

const store2 = useAccountStore()

const recommend = store2.images.main_page.recommend
const exchange = store2.images.main_page.exchange
const map = store2.images.main_page.map

const goFinance = () => {
  router.push({ name: 'deposit' })
}
const goRecommend = () => {
  router.push({ name: 'algo1' })
}
const goExchange = () => {
  router.push({ name: 'exchange' })
}
const goMap = () => {
  router.push({ name: 'map' })
}
</script>





<style scoped>
article {
  margin: auto;
  padding: 30px 0;
  /* background-color: rgb(220, 245, 255); */
}
button {
  width: 180px;
  height: 37px;
  margin: 0;
  padding: 0;
  /* border: 1px solid rgb(15, 137, 255); */
  border-style: none;
  border-radius: 15px;
  font-size: 15px;
  background-color: rgb(2, 2, 2);
  color: white;
}

.content {
  display: flex;
  justify-content: space-between;
  padding: 100px 70px;

  /* border: 1px solid rgb(226, 226, 226); */
  border-radius: 10px;
  width: 1200px;
}

.even-content {
  background-color: rgb(249, 252, 253);
}


.info-box {
  padding-top: 10px;
  min-width: 450px;
}

.recommend-img {
  width: 400px;
  border-radius: 15px;
  box-shadow: 5px 5px 10px rgba(0, 0, 0, 0.5);
}

.title {
  font-family: 'S-CoreDream-6Bold';
  color: rgb(0, 124, 173);
  font-size: 17px;
  padding-top: 10px;
}

.title2 {
  font-family: 'S-CoreDream-6Bold';
  font-size: 28px;
}

.title-right {
  font-family: 'S-CoreDream-6Bold';
  color: rgb(96, 170, 0);
  font-size: 17px;
  padding-top: 10px;
}

.sub-txt {
  color: rgb(99, 99, 99);
  margin-bottom: 10px;
}

.content-name {
  font-family: 'S-CoreDream-6Bold';
  margin-top: 10px;
  font-size: 18px;
}

.product-switch {
  margin: 10px 5px;
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

.pdt-deposit {
  cursor: pointer;
  border: 1px solid rgb(15, 137, 255);
  border-radius: 10px 0 0 10px;
  padding-left: 10px;
  padding-right: 5px;

}
.pdt-saving {
  cursor: pointer;
  color: white;
  border: 1px solid rgb(15, 137, 255);
  background-color: rgb(15, 137, 255);
  border-radius: 0 10px 10px 0;
  padding-left: 5px;
  padding-right: 10px;

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