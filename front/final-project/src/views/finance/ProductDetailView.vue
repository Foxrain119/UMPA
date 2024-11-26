<template>
  <div class="product-detail">
    <p class="cursor" @click.prevent="goBack">← 뒤로가기</p>
    <h2>{{ detail.fin_prdt_nm }}</h2>
    <p>{{ detail.kor_co_nm }}</p>
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
          <tr v-for="option in sortedOptions" :key="option.save_trm">
            <td>{{ option.save_trm }}개월</td>
            <td>{{ option.intr_rate_type_nm }}</td>
            <td>{{ option.intr_rate }}%</td>
            <td>{{ option.intr_rate2 }}%</td>
          </tr>
        </tbody>
      </table>
    </div>
    <div class="product-actions">
      <template v-if="accountStore.isLogin">
        <button 
          v-if="isAlreadyJoined"
          @click="handleCancelProduct" 
          class="cancel-btn"
        >
          관심 상품 취소하기
        </button>
        <button 
          v-else
          @click="handleJoinProduct" 
          class="join-btn"
        >
          관심 상품에 추가
        </button>
      </template>
      <p v-else class="login-message">
        상품 비교를 위해서는 <router-link to="/login">로그인</router-link>이 필요합니다.
      </p>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useFinanceStore } from '@/stores/finance'
import { useAccountStore } from '@/stores/account'
import { useRouter, useRoute } from 'vue-router'

const store = useFinanceStore()
const accountStore = useAccountStore()
const router = useRouter()
const route = useRoute()

const detail = computed(() => store.detail)
const isDataLoaded = ref(false)

// 상품 정보 로드 함수 수정
const loadProductDetail = async (productId) => {
  try {
    const productData = await store.getProductDetail(productId)
    
    // 상품 타입 판별 로직 수정
    const productType = productData.rsrv_type_nm ? 'saving' : 'deposit'
    console.log('Product Type Detection:', {
      rsrv_type_nm: productData.rsrv_type_nm,
      detectedType: productType
    })
    
    store.detail = {
      ...productData,
      product_type: productType
    }

    // 프로필 정보도 함께 갱신
    if (accountStore.isLogin) {
      await accountStore.getProfile()
      console.log('Profile after load:', accountStore.profile)
    }
  } catch (error) {
    console.error('상품 정보 로드 실패:', error)
    throw error
  }
}

// isAlreadyJoined computed 속성 수정
const isAlreadyJoined = computed(() => {
  if (!isDataLoaded.value || !accountStore.profile) {
    console.log('데이터가 아직 로드되지 않음')
    return false
  }

  // profile 객체 구조 로깅
  console.log('Profile structure:', {
    profile: accountStore.profile,
    joined_deposits: accountStore.profile.joined_deposits,
    joined_savings: accountStore.profile.joined_savings
  })

  // 상품 타입에 따른 가입 상품 목록 선택
  const joinedProducts = detail.value.product_type === 'deposit' ? 
    accountStore.profile.joined_deposits : accountStore.profile.joined_savings

  // 가입 여부 체크 로직 개선
  const isJoined = joinedProducts?.some(p => {
    console.log('Comparing:', {
      joined: p.fin_prdt_cd,
      current: detail.value.fin_prdt_cd,
      match: p.fin_prdt_cd === detail.value.fin_prdt_cd
    })
    return p.fin_prdt_cd === detail.value.fin_prdt_cd
  })

  console.log('Join Check Result:', {
    productCode: detail.value.fin_prdt_cd,
    type: detail.value.product_type,
    joinedProducts: joinedProducts?.map(p => p.fin_prdt_cd),
    isJoined
  })

  return isJoined
})

// 프로필 정보 로드 함수 분리
const loadProfileData = async () => {
  if (accountStore.isLogin) {
    await accountStore.getProfile()
    console.log('Profile loaded with products:', {
      deposits: accountStore.profile.joined_deposits,
      savings: accountStore.profile.joined_savings
    })
  }
}

// 컴포넌트 마운트 시 데이터 로드 순서 보장
onMounted(async () => {
  const productId = route.params.productId
  if (!productId) return

  try {
    isDataLoaded.value = false
    console.log('1. 데이터 로드 시작')

    // 1. 먼저 프로필 정보를 가져옴
    await loadProfileData()
    console.log('2. 프로필 정보 로드 완료')
    
    // 2. 그 다음 상품 정보를 가져옴
    await loadProductDetail(productId)
    console.log('3. 상품 정보 로드 완료')

    isDataLoaded.value = true
    console.log('4. 모든 데이터 로드 완료')

  } catch (error) {
    console.error('데이터 로드 실패:', error)
    window.alert('정보를 불러오는데 실패했습니다.')
  }
})

// 옵션 정렬
const sortedOptions = computed(() => {
  if (!detail.value.option) return []
  return [...detail.value.option].sort((a, b) => {
    if (a.save_trm && b.save_trm) {
      return a.save_trm - b.save_trm
    }
    return 0
  })
})

const joinDeny = function () {
  if (detail.value.join_deny === 1) return '제한 없음'
  else if (detail.value.join_deny === 2) return '서민 전용'
  else return '일부 제한'
}

const goBack = () => {
  store.goBack()
}

// 상품 가입/취소 후 상태 업데이트 함수
const updateProfileAndStore = async () => {
  await accountStore.getProfile()
  await loadProductDetail(route.params.productId)
}

// 상품 가입 처리 함수
const handleJoinProduct = async () => {
  if (!accountStore.isLogin) {
    window.alert('로그인이 필요합니다.')
    router.push({ name: 'login' })
    return
  }

  try {
    const productData = {
      fin_prdt_cd: detail.value.fin_prdt_cd,
      fin_prdt_nm: detail.value.fin_prdt_nm,
      kor_co_nm: detail.value.kor_co_nm,
      product_type: detail.value.product_type
    }
    
    await accountStore.joinProduct(productData)
    await updateProfileAndStore()
    window.alert('상품 추가가 완료되었습니다.')
  } catch (error) {
    console.error('상품 가입 실패:', error)
    window.alert(error.response?.data?.error || '상품 가입에 실패했습니다.')
  }
}

// 상품 가입 취소 처리 함수
const handleCancelProduct = async () => {
  if (!window.confirm('정말 이 상품을 관심 목록에서 취소하시겠습니까?')) {
    return
  }

  try {
    await accountStore.cancelProduct(detail.value.fin_prdt_cd, detail.value.product_type)
    await updateProfileAndStore()
    window.alert('상품 가입이 취소되었습니다.')
  } catch (error) {
    console.error('상품 가입 취소 실패:', error)
    window.alert('상품 가입 취소에 실패했습니다.')
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

.cancel-btn {
  padding: 0.8rem 2rem;
  background-color: #dc3545;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1.1rem;
  transition: background-color 0.3s ease;
}

.cancel-btn:hover {
  background-color: #c82333;
}
</style>