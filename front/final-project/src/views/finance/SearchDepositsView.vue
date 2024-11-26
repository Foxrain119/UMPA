<template>
  <div class="search-container">
    <form @submit.prevent="searchingDeposit" class="search-form">
      <div class="form-group">
        <label for="period">기간 :</label>
        <select name="period" id="period" v-model="period">
          <option :value="null">전체</option>
          <option value="1">1개월</option>
          <option value="3">3개월</option>
          <option value="6">6개월</option>
          <option value="12">12개월</option>
          <option value="24">24개월</option>
          <option value="36">36개월</option>
        </select>
      </div>

      <div class="form-group">
        <label for="rateMethod">이자 계산 방식 :</label>
        <select name="rateMethod" id="rateMethod" v-model="rateMethod">
          <option :value="null">전체</option>
          <option value="단리">단리</option>
          <option value="복리">복리</option>
        </select>
      </div>

      <div class="form-group">
        <label for="maxLimit">최고 한도 :</label>
        <input type="number" id="maxLimit" name="maxLimit" v-model="maxLimit">
      </div>

      <div class="form-group">
        <label for="rate">저축 금리 :</label>
        <input type="number" id="rate" name="rate" v-model="rate" step="0.01">
      </div>
      
      <div class="form-group">
        <label for="keyword">검색어 :</label>
        <input type="text" id="keyword" name="keyword" v-model="keyword">
      </div>
      
      <div class="form-group submit-group">
        <input type="submit" value="검색" class="search-btn">
      </div>
    </form>

    <table class="table">
      <thead>
        <tr>
          <th class="product-name">상품명</th>
          <th class="bank-name">금융회사</th>
          <th class="rate-col">6개월</th>
          <th class="rate-col">12개월</th>
          <th class="rate-col">24개월</th>
          <th class="rate-col">36개월</th>
          <th class="detail-col">상세정보</th>
        </tr>
      </thead>
      <tbody>
        <ProductItem
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
import ProductItem from '@/components/finance/ProductItem.vue';
import { computed, ref, onMounted } from 'vue'
import { useFinanceStore } from '@/stores/finance';

const store = useFinanceStore()

onMounted(async () => {
  await store.getProducts()
})

const deposits = ref(store.deposits.sort(function (a, b) {
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
}))

const searchedDeposit = ref()
searchedDeposit.value = deposits.value

// 검색 조건
const period = ref(null)
const rateMethod = ref(null)
const maxLimit = ref(null)
const rate = ref(null)
const keyword = ref(null)

// 기존 검색 알고리즘 유지
const searchingDeposit = function () {
  let searched = deposits.value
  if (period.value) {
    searched = searched.filter((el) => {
      return el.option.some((el) => {
        return el.save_trm.toString() === period.value
      })
    })
  }
  if (rateMethod.value) {
    searched = searched.filter((el) => {
      return el.option.some((el) => el.intr_rate_type_nm === rateMethod.value)
    })
  }
  if (maxLimit.value) {
    searched = searched.filter((el) => {
      return !el.max_limit || el.max_limit >= maxLimit.value
    })
  }
  if (rate.value) {
    searched = searched.filter((el) => {
      return el.option.some((el) => el.intr_rate2 >= rate.value)
    })
  }
  if (keyword.value) {
    searched = searched.filter((el) => {
      return Object.values(el).some((value) => {
        if (typeof value === "string") {
          return value.includes(keyword.value)
        } else if (typeof value === "number") {
          return value.toString().includes(keyword.value)
        } else if (Array.isArray(value)) {
          return value.some(item => item.toString().includes(keyword.value))
        }
        return false
      })
    })
    keyword.value = null
  }
  searchedDeposit.value = searched
  currentPage.value = 1
}

const currentPage = ref(1)
const productCount = 15
const totalPage = computed(() => Math.ceil(searchedDeposit.value.length / productCount))

const displayedProducts = computed (() => {
  const startIdx = (currentPage.value - 1) * productCount
  const endIdx = startIdx + productCount
  return searchedDeposit.value.slice(startIdx, endIdx)
})

const prePage = () => {
  currentPage.value -= 1
}

const nextPage = () => {
  currentPage.value += 1
}
</script>

<style scoped>
.search-container {
  padding: 1rem;
}

.search-form {
  display: flex;
  flex-wrap: wrap;
  gap: 1.5rem;
  background-color: #f8f9fa;
  padding: 1.5rem;
  border-radius: 8px;
  margin-bottom: 2rem;
}

.form-group {
  display: flex;
  align-items: center;
  gap: 0.8rem;
}

.form-group label {
  color: #333;
  font-size: 0.9rem;
  font-weight: 500;
  white-space: nowrap;
}

.form-group input,
.form-group select {
  padding: 0.7rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 0.9rem;
}

.search-btn {
  padding: 0.7rem 2rem;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background-color 0.3s ease;
}

.search-btn:hover {
  background-color: #0056b3;
}

/* 테이블 스타일 */
.table {
  width: 100%;
  border-collapse: collapse;
}

.table th {
  background-color: #f8f9fa;
  padding: 0.8rem;
  text-align: left;
  border-bottom: 2px solid #dee2e6;
  white-space: nowrap;
}

/* 컬럼 너비 조정 */
.product-name {
  width: 25%;
}

.bank-name {
  width: 20%;
}

.rate-col {
  width: 10%;
  font-size: 0.9rem;
  text-align: center;
}

.detail-col {
  width: 8%;
  font-size: 0.9rem;
  text-align: center;
  padding: 0.5rem;
}

/* 페이지네이션 버튼 */
.page_btn {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  margin-top: 2rem;
}

.left-btn, .right-btn {
  padding: 0.5rem 1rem;
  border: none;
  background-color: #007bff;
  color: white;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.left-btn:hover, .right-btn:hover {
  background-color: #0056b3;
}

/* 반응형 디자인 */
@media (max-width: 768px) {
  .search-form {
    grid-template-columns: 1fr;
  }
}
</style>
