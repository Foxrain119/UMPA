<template>
  <tr class="product-row">
    <td class="product-name">{{ product.fin_prdt_nm }}</td>
    <td class="bank-name">{{ product.kor_co_nm }}</td>
    <td class="rate-col">{{ getOptionRate(6) }}</td>
    <td class="rate-col">{{ getOptionRate(12) }}</td>
    <td class="rate-col">{{ getOptionRate(24) }}</td>
    <td class="rate-col">{{ getOptionRate(36) }}</td>
    <td class="detail-col">
      <button @click="showDetail" class="detail-btn">상세정보</button>
    </td>
  </tr>
</template>

<script setup>
import { useFinanceStore } from '@/stores/finance'
import { useRouter } from 'vue-router'

const financeStore = useFinanceStore()
const router = useRouter()

const props = defineProps({
  product: {
    type: Object,
    required: true
  },
  type: {
    type: String,
    required: true
  }
})

const getOptionRate = (term) => {
  const option = props.product.option?.find(el => el.save_trm === term)
  return option ? `${option.intr_rate2}%` : '-'
}

const showDetail = () => {
  const productType = props.product.rsrv_type_nm ? 'saving' : 'deposit'
  console.log('Product Type in ProductItem:', productType)
  
  financeStore.goDetail({
    ...props.product,
    product_type: productType
  })
}
</script>

<style scoped>
.product-row {
  border-bottom: 1px solid #dee2e6;
}

.product-name, .bank-name {
  padding: 0.8rem;
  text-align: left;
}

.rate-col {
  padding: 0.8rem;
  text-align: center;
  font-size: 0.9rem;
}

.detail-col {
  padding: 0.8rem;
  text-align: center;
  white-space: nowrap;
}

.detail-btn {
  padding: 0.4rem 0.8rem;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.85rem;
  transition: background-color 0.3s ease;
}

.detail-btn:hover {
  background-color: #0056b3;
}
</style>