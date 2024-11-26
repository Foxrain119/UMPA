<template>
  <div class="banner">
    <button><</button>
    <a href="https://www.kbstar.com/">
      <img :src="gukmin" alt="gukmin">
    </a>
    <a href="https://www.kebhana.com/">
      <img :src="hana" alt="hana">
    </a>
    <a href="https://www.wooribank.com/">
      <img :src="uri" alt="uri">
    </a>
    <a href="https://www.shinhan.com/">
      <img :src="sinhan" alt="sinhan">
    </a>
    <a href="https://www.nhbank.com/">
      <img :src="nong" alt="nong">
    </a>
    <button>></button>
  </div>
</template>

<script setup>
// import ExchangeSideBar from '@/components/exchange/ExchangeSideBar.vue';
import { useAccountStore } from '@/stores/account';
import { useRouter } from 'vue-router/dist/vue-router';

const store2 = useAccountStore()

const gukmin = store2.images.bank.gukmin
const hana = store2.images.bank.hana
const uri = store2.images.bank.uri
const sinhan = store2.images.bank.sinhan
const nong = store2.images.bank.nong
</script>

<style scoped>
button {
  border-style: none;
  background-color: white;
  font-weight: bold;
}
img {
  width: 80px;
  box-shadow: 2px 4px 4px rgba(158, 158, 158, 0.5);
  border-radius: 18px;
  margin-right: 20px;
}
.banner {
  display: flex;
  justify-content: center;
  margin: 30px 0;
}
</style>