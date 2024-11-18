<template>
  <div>
    <table class="table">
      <thead>
        <tr>
          <th scope="col">순위</th>
          <th scope="col">상품명</th>
          <th scope="col">금융회사</th>
          <th scope="col">6개월</th>
          <th scope="col">12개월</th>
          <th scope="col">24개월</th>
          <th scope="col">36개월</th>
        </tr>
      </thead>
      <tbody>
        <ProductList
          v-for="product in deposits"
          :key="`deposit${deposits.id}`"
          :product="product"
          :options="options.filter(el => el['deposit'] === product.id)"
        />
      </tbody>
    </table>
  </div>
</template>

<script setup>
import ProductList from '@/components/fianance/ProductList.vue';
import { useFinanceStore } from '@/stores/finance';

const store = useFinanceStore()
const deposits = store.deposits
const options = store.deposit_options
</script>

<style scoped>

</style>
