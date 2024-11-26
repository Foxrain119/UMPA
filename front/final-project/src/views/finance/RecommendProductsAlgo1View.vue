<template>
  <div v-if="token && profile" class="algo-box">
    <!-- 추천 상품 목록 -->
     <br>
    <div v-if="recommendDeposit && recommendSaving" class="recommend-box">
      <div class="title"><span class="user-name">{{ profile.nickname }}</span> 님과 비슷한 유저의 인기 가입 상품 top 5</div>
      <br>
      <div>
        <p class="title2">예금 추천 TOP 5</p>
        <div class="dct-bar">
          <p style="margin: 0 20px; padding-left: 5px;">순위</p>
          <p style="margin: 0 38px;">상품명</p>
          <p style="margin: 0 110px;">은행명</p>
          <p style="margin: 0 20px;">금리</p>
        </div>
        <div 
        class="card card-wth row"
          v-for="(product, index) in recommendDeposit"
          :key="index"
          @click.prevent="goDetail(product)"
        >
          <div class="card-detail">
          <p style="margin: 0 10px;">{{ index + 1 }}위</p>
          <p class="pdt-name">{{ product.fin_prdt_nm }}</p>
          <p class="pdt-bank">{{ product.kor_co_nm }}</p>
          <p>{{ product.option.reduce((max, cur) => {
                return cur.intr_rate2 > max ? cur.intr_rate2 : max;
              }, product.option[0]?.intr_rate2 || 0) }}%</p>
          <p></p>
          </div>
        </div>
      </div>
      <br><br>
      <div>
        <p class="title2">적금 추천 TOP 5</p>
        <div class="dct-bar">
          <p style="margin: 0 20px; padding-left: 5px;">순위</p>
          <p style="margin: 0 38px;">상품명</p>
          <p style="margin: 0 110px;">은행명</p>
          <p style="margin: 0 20px;">금리</p>
        </div>
        <div 
        class="card card-wth row"
        v-for="(product, index) in recommendSaving"
        :key="index"
          @click.prevent="goDetail(product)"
        >
          <div class="card-detail">
          <p style="margin: 0 10px;">{{ index + 1 }}위</p>
          <p class="pdt-name">{{ product.fin_prdt_nm }}</p>
          <p class="pdt-bank">{{ product.kor_co_nm  }}</p>
          <p>{{ product.option.reduce((max, cur) => {
                return cur.intr_rate2 > max ? cur.intr_rate2 : max;
              }, product.option[0].intr_rate2) }}%</p>
          </div>
        </div>
      </div>
    </div>
    <br>
    <div class="search-box">
      <p></p>
      <form class="search-condition" @submit.prevent="recommend">
        
        <div class="form-group">
          <label for="marital_status">결혼 여부 :</label>
          <select name="marital_status" id="marital_status" v-model="marital_status">
            <option value="null">전체</option>
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

        <div class="form-group">
          <label for="age">나이 :</label>
          <input type="number" id="age" name="age" v-model="age" min="20">

          <label for="age_range">나이 범위 :</label>
          <select name="age_range" id="age_range" v-model="ageRange">
            <option :value="0">동갑</option>
            <option :value="3">3세 ({{ age - 3 }}~{{ age + 3 }})</option>
            <option :value="5">5세 ({{ age - 5 }}~{{ age + 5 }})</option>
            <option :value="7">7세 ({{ age - 7 }}~{{ age + 7 }})</option>
            <option :value="10">10세 ({{ age - 10 }}~{{ age + 10 }})</option>
          </select>
        </div>

        <div class="form-group submit-group">
          <label for="property">자본 :</label>
          <input type="number" id="property" name="property" v-model="property" min="0"><span></span>
          <label for="property_range">자본 범위(%) :</label>
          <input type="number" id="property_range" name="property_range" v-model="propertyRange" min="1" max="50">
        </div>
        
        <div class="form-group submit-group">
          <input type="submit" value="재추천" class="search-btn">
        </div>
      </form>
    </div>

  </div>

  <div v-if="!token || !profile" class="rqr-login">
    <p>로그인이 필요한 서비스입니다.</p>
  </div>
</template>


<script setup>
import { computed, ref, onMounted } from 'vue'
import { useAccountStore } from '@/stores/account';
import { useFinanceStore } from '@/stores/finance';

const store = useFinanceStore()
const store2 = useAccountStore()

const token = store2.token

onMounted(() => {
  if (token) {
    store2.getProfile();
    recommend()
  }
})

const userInfo = store2.userInfo
const profile = store2.profile

const marital_status = ref(profile?.marital_status)
const age = ref(profile?.age)
const ageRange = ref(0)
const gender = ref(profile?.gender)
const property = ref(profile?.property)
const propertyRange = ref(5)

const deposits = store.deposits
const savings = store.savings

const recommendDeposit = ref(null)
const recommendSaving = ref(null)


const recommend = function () {
  let info = store2.userInfo
  console.log(info)
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
  recommendDeposit.value = recommend_deposit
  recommendSaving.value = recommend_saving

}




const goDetail = (product) => {
  store.goDetail(product)
}

</script>


<style scoped>
.algo-box {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  margin: 0;
  gap: 30px;
}
.recommend-box {
  width:1000px;
  display: flex;
  flex-direction: column;
  align-items: center;
  /* box-shadow: 5px 5px 10px rgba(109, 106, 106, 0.5); */

}
.search-box {
  position: relative;
  width:900px;
  /* margin: 0 auto; */
}
.search-condition {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  background-color: #f8f9fa;
  padding: 1rem;
  border-radius: 8px;
  margin-bottom: 2rem;
  box-shadow: 4px 4px 10px rgba(161, 159, 159, 0.5);
}
.form-group {
  display: flex;
  align-items: center;
  gap: 0.8rem;
}
.form-group label {
  color: #333;
  font-size: 17px;
  font-weight: 500;
  white-space: nowrap;
}

.form-group input,
.form-group select {
  padding: 5px 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
}
.submit-group {
  width: 800px;
  margin: auto;
}

.search-btn {
  width: 80px;
  height: 45px;
  padding: 0;
  margin: auto;
  background-color: #2b92ff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 17px;
  transition: background-color 0.3s ease;
}
.user-name {
  color: rgb(65, 141, 255);
  font-size: 28px;
}
.title {
  font-family: 'S-CoreDream-6Bold';
  /* color: rgb(0, 124, 173); */
  font-size: 20px;
  padding: 10px 0;
  margin-bottom: 30px;
  text-align: center;
  width: 550px;

  border-radius: 15px;
  box-shadow: 0px 2px 10px rgba(66, 14, 255, 0.5);

}
.title2 {
  font-family: 'S-CoreDream-6Bold';
  font-size: 22px;
  padding-top: 10px;
  width: 600px;
}

.dct-bar {
  display: flex;
  margin-bottom: 10px;
}
.card-wth {
  cursor: pointer;
  width: 600px;
  font-size: 17px;
  padding: 6px 0;
  box-shadow: 3px 3px 5px rgba(161, 161, 161, 0.5);
  margin: 0 5px;
  margin-bottom: 10px; 
  border-color: rgb(248, 248, 248);
  background-color: #f9fcff;
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
  width: 200px;
  padding: 0 10px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.pdt-bank {
  width: 220px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.rqr-login {
  margin-top: 200px;
  text-align: center;
  font-size: 20px;
  
}
</style>