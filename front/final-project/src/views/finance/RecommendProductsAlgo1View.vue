<template>
  <div v-if="token && profile">
    <div class="search-box">
      <form class="search-condition" @submit.prevent="recommend">
        <div>{{ userInfo.nickname }}님과 비슷한 유저의 인기 가입 상품 top 5</div>

        <div>
          <label for="marital_status">결혼 여부 :</label>
          <select name="marital_status" id="marital_status" v-model="marital_status">
            <option :value="null">전체</option>
            <option :value="false">미혼</option>
            <option :value="true">기혼</option>
          </select>
    
          <label for="gender">성별 :</label>
          <select name="gender" id="gender" v-model="gender">
            <option value="N">전체</option>
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

    <!-- 추천 상품 목록 -->
    <div>
      <div>
        <p>예금 추천 top 5</p>
        <div 
        class="card card-wth m-1 row"
          v-for="c in 5"
          :key="c"
          @click.prevent="goDetail(recommendProducts[c-1])"
        >
          <div class="card-detail">
          <p style="margin-right: 10px;">{{ c }}</p>
          <p class="pdt-name">{{ recommendProducts[c-1].fin_prdt_nm }}</p>
          <p class="pdt-bank">{{ recommendProducts[c-1].kor_co_nm }}</p>
          <p>{{ recommendProducts[c-1].option.reduce((max, cur) => {
                return cur.intr_rate2 > max ? cur.intr_rate2 : max;
              }, recommendProducts[c-1].option[0].intr_rate2) }}%</p>
          </div>
        </div>
      </div>
  
      <div>
        <p>적금 추천 top 5</p>
        <div 
        class="card card-wth m-1 row"
          v-for="c in 5"
          :key="c"
          @click.prevent="goDetail(recommendProducts[c+4])"
        >
          <div class="card-detail">
          <p style="margin-right: 10px;">{{ c }}</p>
          <p class="pdt-name">{{ recommendProducts[c+4].fin_prdt_nm }}</p>
          <p class="pdt-bank">{{ recommendProducts[c+4].kor_co_nm }}</p>
          <p>{{ recommendProducts[c+4].option.reduce((max, cur) => {
                return cur.intr_rate2 > max ? cur.intr_rate2 : max;
              }, recommendProducts[c+4].option[0].intr_rate2) }}%</p>
          </div>
        </div>
      </div>
    </div>
  </div>

  <div v-if="!token">
    <p>로그인이 필요합니다</p>
  </div>
</template>


<script setup>
import { computed, ref } from 'vue'
import { useAccountStore } from '@/stores/account';
import { useFinanceStore } from '@/stores/finance';
// import { onMounted } from 'vue';

const store = useFinanceStore()
const store2 = useAccountStore()

// onMounted(() => {
//   store2.getProfile()
// })

const userInfo = store2.userInfo
const profile = store2.profile
const token = store2.token

const marital_status = ref(profile.marital_status)
const age = ref(profile.age)
const ageRange = ref(0)
const gender = ref(profile.gender)
const property = ref(profile.property)
const propertyRange = ref(5)

const deposits = store.deposits
const savings = store.savings

const recommendProducts = ref(deposits.slice(0,5).concat(savings.slice(0,5)))

const recommend = function () {
  let info = store2.userInfo
  if (marital_status.value) {
    info = info.filter((el) => {
      return el.marital_status === marital_status.value
    })
  }
  if (age.value) {
    info = info.filter((el) => {
      return el.age >= age.value - ageRange.value && el.age <= age.value + ageRange.value
    })
  }
  if (gender.value !== 'N') {
    info = info.filter((el) => {
      return el.gender === gender.value
    })
  }
  if (property.value) {
    info = info.filter((el) => {
      return el.property <= property.value * (1 + 0.01 * propertyRange.value) && el.property >= property.value * (1 - 0.01 * propertyRange.value)
    })
  }
  
  const deposit_count = new Array(285).fill(0);
  const saving_count = new Array(197).fill(0);

  info.forEach(el => {
    el.joined_deposits.forEach(el => {
      deposit_count[el.id]++;
    });
    el.joined_savings.forEach(el => {
      saving_count[el.id]++;
    });
  });

  const top5_deposits = deposit_count
    .map((val, idx) => ({ val, idx }))
    .sort((a, b) => b.val - a.val)
    .slice(0, 5)
    .map(item => item.idx);
  
  const top5_savings = saving_count
    .map((val, idx) => ({ val, idx }))
    .sort((a, b) => b.val - a.val)
    .slice(0, 5)
    .map(item => item.idx);
  
  let recommend_deposit = deposits.filter((el) => {
    return top5_deposits.includes(el.id)
  })
  recommend_deposit = recommend_deposit.sort(function (a, b) {
    const optionA = a.option.reduce((max, cur) => {
      return cur.intr_rate2 > max.intr_rate2 ? cur : max;
    }, a.option[0])
    const optionB = b.option.reduce((max, cur) => {
      return cur.intr_rate2 > max.intr_rate2 ? cur : max;
    }, b.option[0])

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
  let recommend_saving = savings.filter((el) => {
    return top5_savings.includes(el.id)
  })
  recommend_saving = recommend_saving.sort(function (a, b) {
    const optionA = a.option.reduce((max, cur) => {
      return cur.intr_rate2 > max.intr_rate2 ? cur : max;
    }, a.option[0])
    const optionB = b.option.reduce((max, cur) => {
      return cur.intr_rate2 > max.intr_rate2 ? cur : max;
    }, b.option[0])

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
  recommendProducts.value = recommend_deposit.concat(recommend_saving)
}




const goDetail = (product) => {
  store.goDetail(product)
}

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