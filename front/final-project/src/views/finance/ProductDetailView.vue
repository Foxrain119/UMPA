<template>
  <div>
    <p class="cursor" @click.prevent="goBack">← 뒤로가기</p>
    <h2>{{ detail.fin_prdt_nm }}</h2>
    <p>{{ detail.kor_co_nm }}</p>
    <!-- <span
      v-for="option in detail.option"
    >{{ option.save_trm }}개월</span><br><br> -->
    <p>최고 한도 : {{ detail.max_limit ? detail.max_limit : '없음' }}</p>
    <p>가입 대상 : {{ detail.join_member }}</p>
    <p>가입 제한 : {{ joinDeny() }}</p>
    <p>가입 방법 : {{ detail.join_way }}</p>
    <p>상세 정보</p>
    <p>{{ detail.etc_note }}</p>
    <p>우대 조건</p>
    <p>{{ detail.spcl_cnd }}</p>
    <div class="option-detail">
      <table class="table">
        <thead>
          <tr>
            <th scope="col">기간</th>
            <th scope="col">금리 유형</th>
            <th scope="col">저축 금리</th>
            <th scope="col">최고 우대금리</th>
          </tr>
        </thead>
  
        <tbody>
          <tr
            v-for="option in options"
          >
            <td>{{ option.save_trm }}개월</td>
            <td>{{ option.intr_rate_type_nm }}</td>
            <td>{{ option.intr_rate }}%</td>
            <td>{{ option.intr_rate2 }}%</td>
          </tr>
        </tbody>
      </table>
    </div>
    <div class="product-actions">
      <button 
        v-if="accountStore.isLogin"
        @click="handleJoinProduct" 
        :disabled="isAlreadyJoined"
        class="join-btn"
        :class="{ 'disabled': isAlreadyJoined }"
      >
        {{ isAlreadyJoined ? '이미 가입한 상품입니다' : '상품 가입하기' }}
      </button>
      <p v-else class="login-message">
        상품 가입을 위해서는 <router-link to="/login">로그인</router-link>이 필요합니다.
      </p>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useFinanceStore } from '@/stores/finance';
import { useAccountStore } from '@/stores/account'
import { useRouter, useRoute } from 'vue-router'

const store = useFinanceStore()
const accountStore = useAccountStore()
const router = useRouter()
const route = useRoute()

const detail = store.detail

const options = detail.option.sort(function (a, b) {
  const optionA = a.save_trm;
  const optionB = b.save_trm;

  if (optionA && optionB) {
    return optionA - optionB;
  } else if (optionA) {
    return 1;
  } else if (optionB) {
    return -1;
  } else {
    return 0;
  }
});
const joinDeny = function () {
  if (detail.join_deny === 1) {
    return '제한 없음'
  }
  else if (detail.join_deny === 2) {
    return '서민 전용'
  }
  else {
    return '일부 제한'
  }
}

const goBack = () => {
  store.goBack()
}

const isAlreadyJoined = computed(() => {
  const profile = accountStore.profile
  if (!profile) return false

  const productType = detail.product_type
  const joinedProducts = productType === 'deposit' ? 
    (profile.joined_deposits || []) : 
    (profile.joined_savings || [])

  return joinedProducts.some(p => p.fin_prdt_cd === detail.fin_prdt_cd)
})

const productType = computed(() => {
  console.log('Current route:', route.path, route.name) // 디버깅용
  console.log('Detail data:', detail) // 디버깅용
  
  // detail에서 직접 product_type 가져오기
  return detail.product_type || null
})

const handleJoinProduct = async () => {
  if (!accountStore.isLogin) {
    window.alert('로그인이 필요합니다.')
    router.push({ name: 'login' })
    return
  }

  if (isAlreadyJoined.value) {
    window.alert('이미 가입한 상품입니다.')
    return
  }

  try {
    const productData = {
      fin_prdt_cd: detail.fin_prdt_cd,
      fin_prdt_nm: detail.fin_prdt_nm,
      kor_co_nm: detail.kor_co_nm,
      product_type: detail.product_type
    }
    
    await accountStore.joinProduct(productData)
    window.alert('상품 가입이 완료되었습니다.')
    await accountStore.getProfile()  // 프로필 정보 즉시 갱신
  } catch (error) {
    if (error.response?.data?.error === '이미 가입한 상품입니다.') {
      window.alert('이미 가입한 상품입니다.')
    } else {
      window.alert('상품 가입에 실패했습니다.')
      console.error('상품 가입 오류:', error)
    }
  }
}

</script>

<style scoped>
td {
  width: 20px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.cursor {
  cursor: pointer;
}
.option-detail {
  width: 600px;
}
.product-actions {
  margin-top: 2rem;
  text-align: center;
}

.join-btn {
  padding: 0.8rem 2rem;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1.1rem;
}

.join-btn:hover {
  background-color: #0056b3;
}

.login-message {
  color: #666;
}

.login-message a {
  color: #007bff;
  text-decoration: underline;
}

.join-btn.disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.join-btn:disabled {
  opacity: 0.7;
}
</style>