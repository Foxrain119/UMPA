<template>
  <div class="products-container">
    <!-- 가입한 상품 목록 -->
    <div class="joined-products">
      <h3>관심있는 예금 상품들</h3>
      <div class="product-list">
        <!-- 예금 상품 목록 -->
        <div v-if="profile?.joined_deposits?.length" class="product-category">
          <div v-for="(product, index) in profile.joined_deposits" 
               :key="`deposit-${index}`" 
               class="product-item"
          >
            <span>{{ index + 1 }} : {{ product.kor_co_nm }} - {{ product.fin_prdt_nm }}</span>
            <div class="product-actions">
              <button class="detail-btn" @click="showProductDetail(product, 'deposit')">
                상세 보기
              </button>
              <button class="cancel-btn" @click="cancelProduct(product.fin_prdt_cd, 'deposit')">
                관심 취소하기
              </button>
            </div>
          </div>
        </div>

        <!-- 적금 상품 목록 -->
        <div v-if="profile?.joined_savings?.length" class="product-category">
          <h4>적금 상품</h4>
          <div v-for="(product, index) in profile.joined_savings" 
               :key="`saving-${index}`" 
               class="product-item"
          >
            <span>{{ index + 1 }} : {{ product.kor_co_nm }} - {{ product.fin_prdt_nm }}</span>
            <div class="product-actions">
              <button class="detail-btn" @click="showProductDetail(product, 'saving')">
                상세 보기
              </button>
              <button class="cancel-btn" @click="cancelProduct(product.fin_prdt_cd, 'saving')">
                가입 취소하기
              </button>
            </div>
          </div>
        </div>

        <!-- 가입한 상품이 없는 경우 -->
        <div v-if="!profile?.joined_deposits?.length && !profile?.joined_savings?.length" 
             class="no-products"
        >
          가입한 상품이 없습니다.
        </div>
      </div>
    </div>

    <!-- 금리 비교 그래프 -->
    <div v-if="hasJoinedProducts" class="interest-graph">
      <h3>관심 상품 금리 비교</h3>
      <div class="graph-controls">
        <select v-model="selectedPeriod" class="period-select" @change="updateChart">
          <option value="6">6개월</option>
          <option value="12">12개월</option>
          <option value="24">24개월</option>
          <option value="36">36개월</option>
        </select>

        <select v-model="selectedRateType" class="rate-type-select" @change="updateChart">
          <option value="단리">단리</option>
          <option value="복리">복리</option>
        </select>
      </div>
      <div class="chart-container">
        <canvas ref="chartCanvas"></canvas>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAccountStore } from '@/stores/account'
import { useFinanceStore } from '@/stores/finance'
import Chart from 'chart.js/auto'

const router = useRouter()
const accountStore = useAccountStore()
const financeStore = useFinanceStore()

const props = defineProps({
  profile: {
    type: Object,
    required: true
  }
})

// 차트 관련 상태
const selectedPeriod = ref(6)
const selectedRateType = ref('단리')
const chartCanvas = ref(null)
let chart = null

// 가입한 상품이 있는지 확인
const hasJoinedProducts = computed(() => {
  return (props.profile?.joined_deposits?.length || 0) + 
         (props.profile?.joined_savings?.length || 0) > 0
})

// 금리 유형 정규화 함수 추가
const normalizeRateType = (rateType) => {
  if (!rateType) return ''
  // 공백 제거 및 소문자 변환
  return rateType.trim().toLowerCase()
}

// 차트 데이터 준비 함수 수정
const prepareChartData = () => {
  const depositProducts = props.profile?.joined_deposits || []
  const savingProducts = props.profile?.joined_savings || []
  const allProducts = [...depositProducts, ...savingProducts]
  
  // 선택된 금리 유형에 따라 상품 필터링
  const filteredProducts = selectedRateType.value === 'all' 
    ? allProducts 
    : allProducts.filter(p => {
        const option = p.option?.find(o => {
          if (o.save_trm === -1) return false
          return Number(o.save_trm) === Number(selectedPeriod.value)
        })
        
        // 디버깅용 로그
        console.log('Product Options:', {
          name: p.fin_prdt_nm,
          allOptions: p.option,
          matchingOption: option,
          rateTypes: p.option?.map(o => o.intr_rate_type_nm)
        })
        
        // 해당 상품의 모든 옵션에서 선택된 금리 유형이 있는지 확인
        return p.option?.some(o => 
          normalizeRateType(o.intr_rate_type_nm) === normalizeRateType(selectedRateType.value)
        )
      })

  console.log('Filtered Products:', {
    total: allProducts.length,
    filtered: filteredProducts.length,
    products: filteredProducts.map(p => ({
      name: p.fin_prdt_nm,
      options: p.option?.map(o => ({
        term: o.save_trm,
        rateType: o.intr_rate_type_nm
      }))
    }))
  })

  const labels = filteredProducts.map(p => `${p.kor_co_nm}\n${p.fin_prdt_nm}`)
  
  // 기본 금리와 우대 금리 데이터 (음수 값 제외)
  const baseRates = filteredProducts.map(p => {
    const option = p.option?.find(o => Number(o.save_trm) === Number(selectedPeriod.value))
    const rate = option ? Number(option.intr_rate) : 0
    return rate < 0 ? 0 : rate  // 음수인 경우 0으로 처리
  })

  const specialRates = filteredProducts.map(p => {
    const option = p.option?.find(o => Number(o.save_trm) === Number(selectedPeriod.value))
    const rate = option ? Number(option.intr_rate2) : 0
    return rate < 0 ? 0 : rate  // 음수인 경우 0으로 처리
  })

  return {
    labels,
    datasets: [
      {
        label: `${selectedPeriod.value}개월 기본금리`,
        data: baseRates,
        backgroundColor: 'rgba(54, 162, 235, 0.5)',
        borderColor: 'rgb(54, 162, 235)',
        borderWidth: 1
      },
      {
        label: `${selectedPeriod.value}개월 우대금리`,
        data: specialRates,
        backgroundColor: 'rgba(255, 99, 132, 0.5)',
        borderColor: 'rgb(255, 99, 132)',
        borderWidth: 1
      }
    ]
  }
}

// 차트 업데이트 함수 수정
const updateChart = () => {
  if (chart) {
    chart.destroy()
  }

  if (!chartCanvas.value) {
    console.log('Chart canvas not found')
    return
  }

  const ctx = chartCanvas.value.getContext('2d')
  const chartData = prepareChartData()
  
  // 필터링된 상품 목록 저장 (상태로 관리)
  const filteredProducts = selectedRateType.value === 'all' 
    ? [...(props.profile?.joined_deposits || []), ...(props.profile?.joined_savings || [])]
    : [...(props.profile?.joined_deposits || []), ...(props.profile?.joined_savings || [])].filter(p => {
        const option = p.option?.find(o => Number(o.save_trm) === Number(selectedPeriod.value))
        return option && normalizeRateType(option.intr_rate_type_nm) === normalizeRateType(selectedRateType.value)
      })
  
  chart = new Chart(ctx, {
    type: 'bar',
    data: chartData,
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'top',
        },
        title: {
          display: true,
          text: '가입 상품 금리 비교'
        },
        tooltip: {
          callbacks: {
            afterBody: function(tooltipItems) {
              try {
                // 선택된 금리 유형을 직접 표시
                return `금리 유형: ${selectedRateType.value}`
              } catch (error) {
                console.error('Tooltip error:', error)
                return '금리 유형: 정보 없음'
              }
            }
          }
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          title: {
            display: true,
            text: '금리 (%)'
          }
        }
      }
    }
  })
}

// 상품 상세 정보 보기
const showProductDetail = (product, type) => {
  financeStore.goDetail({
    ...product,
    product_type: type
  })
}

// 상품 가입 취소
const cancelProduct = async (productId, type) => {
  if (!window.confirm('정말 이 상품의 가입을 취소하시겠습니까?')) {
    return
  }

  try {
    await accountStore.cancelProduct(productId, type)
    window.alert('상품 가입이 취소되었습니다.')
    // 프로필 정보 새로고침
    await accountStore.getProfile()
  } catch (error) {
    console.error('상품 가입 취소 실패:', error)
    window.alert('상품 가입 취소에 실패했습니다.')
  }
}

// 컴포넌트 마운트 시 차트 생성
onMounted(() => {
  if (hasJoinedProducts.value) {
    updateChart()
  }
})

// 프로필 데이터가 변경될 때 차트 업데이트
watch(() => props.profile, () => {
  if (hasJoinedProducts.value) {
    updateChart()
  }
}, { deep: true })

// 선택된 기간이 변경될 때 차트 업데이트
watch(selectedPeriod, () => {
  if (hasJoinedProducts.value) {
    updateChart()
  }
})

// 컴포넌트 언마운트 시 차트 정리
onUnmounted(() => {
  if (chart) {
    chart.destroy()
  }
})
</script>

<style scoped>
.products-container {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.joined-products, .interest-graph {
  background: #f8f9fa;
  padding: 1.5rem;
  border-radius: 8px;
}

.product-category {
  margin-bottom: 1.5rem;
}

.product-category h4 {
  margin-bottom: 1rem;
  color: #0066cc;
}

.product-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-top: 1rem;
}

.product-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background: white;
  border-radius: 4px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

.product-actions {
  display: flex;
  gap: 0.5rem;
}

.detail-btn, .cancel-btn {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
}

.detail-btn {
  background: #007bff;
  color: white;
}

.cancel-btn {
  background: #dc3545;
  color: white;
}

.graph-controls {
  display: flex;
  gap: 1rem;
  margin: 1rem 0;
}

.period-select,
.rate-type-select {
  padding: 0.5rem;
  border-radius: 4px;
  border: 1px solid #ddd;
}

.chart-container {
  height: 400px;
  background: white;
  border-radius: 4px;
  padding: 1rem;
  margin-top: 1rem;
}

.no-products {
  text-align: center;
  padding: 2rem;
  color: #666;
  background: white;
  border-radius: 4px;
}
</style> 