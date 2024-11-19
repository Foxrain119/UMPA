<template>
  <div class="search-box">
    <table class="table">
      <thead>
        <tr>
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
          v-for="product in displayedProducts"
          :key="`deposit${product.id}`"
          :product="product"
        />
      </tbody>
    </table>

    <div class="page_btn">
      <button v-show="currentPage > 1" @click.prevent="prePage" class="left-btn"><</button>
      <span>{{ currentPage }} / {{ totalPage }}</span>
      <button v-show="currentPage < totalPage" @click.prevent="nextPage" class="right-btn">></button>
    </div>
  </div>
</template>

<script setup>
import ProductList from '@/components/fianance/ProductItem.vue';
import { computed, ref } from 'vue'
import { useFinanceStore } from '@/stores/finance';

const store = useFinanceStore()

const savings = store.savings.sort(function (a, b) {
  const optionA = a.option.find(opt => opt.save_trm === 6);
  const optionB = b.option.find(opt => opt.save_trm === 6);

  if (optionA && optionB) {
    return optionB.intr_rate2 - optionA.intr_rate2;
  } else if (optionA) {
    return -1;
  } else if (optionB) {
    return 1;
  } else {
    return 0;
  }
})

const currentPage = ref(1)
const productCount = 15
const totalPage = computed(() => Math.floor(savings.length / productCount) + 1)

const displayedProducts = computed (() => {
  const startIdx = (currentPage.value - 1) * productCount
  const endIdx = startIdx + productCount
  return savings.slice(startIdx, endIdx)
})

const prePage = () => {
  currentPage.value -= 1
}

const nextPage = () => {
  currentPage.value += 1
}

</script>

<style scoped>
button {
  position: absolute;
}
.left-btn {
  left: 445px;
}
.right-btn {
  right: 445px
}
.search-box {
  position: relative;
  width: 1000px;
  margin: 0 auto;
}
.page_btn {
  text-align: center;
}
</style>
