<template>
  <tr>
    <!-- <th scope="row"></th> -->
    <td>{{ product['fin_prdt_nm'] }}</td>
    <td>{{ product['kor_co_nm'] }}</td>
    <td>{{ option6 ? `${option6['intr_rate2']}%` : '-' }}</td>
    <td>{{ option12 ? `${option12['intr_rate2']}%` : '-' }}</td>
    <td>{{ option24 ? `${option24['intr_rate2']}%` : '-' }}</td>
    <td>{{ option36 ? `${option36['intr_rate2']}%` : '-' }}</td>
    <button
      @click.prevent="goDetail"
    >상세정보</button>
  </tr>
</template>

<script setup>
import { useFinanceStore } from '@/stores/finance';
const store = useFinanceStore()

const props = defineProps({
  product: Object,
})

const option = props.product.option
const option6 = option.find(el => el['save_trm'] === 6)
const option12 = option.find(el => el['save_trm'] === 12)
const option24 = option.find(el => el['save_trm'] === 24)
const option36 = option.find(el => el['save_trm'] === 36)

const goDetail = () => {
  store.goDetail(props.product)
}

</script>

<style scoped>
td {
  max-width: 100px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
</style>