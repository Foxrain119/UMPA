<template>
  <div class="search-box">
    <!-- 검색창 -->
    <!-- <div class="search-condition">
    </div> -->

    <form class="search-condition" @submit.prevent="searchingDeposit">
      <div>검색창</div>

      <div>
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
  
        <label for="rateMethod">이자 계산 방식 :</label>
        <select name="rateMethod" id="rateMethod" v-model="rateMethod">
          <option :value="null">전체</option>
          <option value="단리">단리</option>
          <option value="복리">복리</option>
        </select>
  
  
        <label for="maxLimit">최고 한도 :</label>
        <input type="number" id="maxLimit" name="maxLimit" v-model="maxLimit">
  
        <label for="rate">저축 금리 :</label>
        <input type="number" id="rate" name="rate" v-model="rate" step="0.01">
      </div>
      
      <div>
        <label for="keyword">검색어 :</label>
        <input type="text" id="keyword" name="keyword" v-model="keyword">
      </div>
      
      <div>
        <input type="submit" value="검색">
      </div>
    </form>

    <table class="table">
      <thead>
        <tr>
          <!-- <th scope="col">순위</th> -->
          <th scope="col">상품명</th>
          <th scope="col">금융회사</th>
          <th scope="col">6개월</th>
          <th scope="col">12개월</th>
          <th scope="col">24개월</th>
          <th scope="col">36개월</th>
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
import ProductItem from '@/components/fianance/ProductItem.vue';
import { computed, ref } from 'vue'
import { useFinanceStore } from '@/stores/finance';

const store = useFinanceStore()
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

// 검색 알고리즘
const period = ref(null)
const rateMethod = ref(null)
const maxLimit = ref(null)
const rate = ref(null)
const keyword = ref(null)

const searchingDeposit = function () {
  let searched =  deposits.value
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
          return value.includes(keyword.value); // 문자열에 검색어 포함 여부 확인
        } else if (typeof value === "number") {
          return value.toString().includes(keyword.value); // 숫자를 문자열로 변환 후 포함 여부 확인
        } else if (Array.isArray(value)) {
          return value.some(item => item.toString().includes(keyword.value)); // 배열 항목에 대해 검색어 포함 여부 확인
        }
      })
    })
    keyword.value = null
  }
  // console.log(deposits.value)
  searchedDeposit.value = searched
  currentPage.value = 1
}


const currentPage = ref(1)
const productCount = 15
const totalPage = computed(() => Math.floor(searchedDeposit.value.length / productCount) + 1)

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
.search-condition {
  border: 1px solid black;
  width: 900px;
}
.page_btn {
  text-align: center;
}
</style>
