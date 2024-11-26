<template>
  <div class="products-container">
    <!-- 가입한 상품 목록 -->
    <div class="joined-products">
      <h3>가입한 상품들</h3>
      <div class="product-list">
        <!-- 예금 상품 목록 -->
        <div v-if="profile?.joined_deposits?.length" class="product-category">
          <h4>예금 상품</h4>
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
                가입 취소하기
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

    <!-- 금리 그래프 -->
    <div class="interest-graph">
      <h3>가입한 상품 금리</h3>
      <div class="graph-controls">
        <select v-model="selectedPeriod" class="period-select" @change="updateChart">
          <option value="3">3개월 금리</option>
          <option value="6">6개월 금리</option>
          <option value="12">12개월 금리</option>
        </select>
      </div>
      <div class="chart-container">
        <canvas ref="chartCanvas"></canvas>
      </div>
    </div>

    <!-- 상품 상세 정보 모달 -->
    <div v-if="showModal" class="modal-overlay" @click="closeModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>상품 상세 정보</h3>
          <button class="close-btn" @click="closeModal">&times;</button>
        </div>
        
        <div v-if="selectedProduct" class="modal-body">
          <div class="product-info">
            <p><strong>은행명:</strong> {{ selectedProduct.kor_co_nm }}</p>
            <p><strong>상품명:</strong> {{ selectedProduct.fin_prdt_nm }}</p>
            <p><strong>상품 코드:</strong> {{ selectedProduct.fin_prdt_cd }}</p>
            
            <!-- 예금 상품인 경우 -->
            <template v-if="selectedProduct.type === 'deposit'">
              <p><strong>가입 방법:</strong> {{ selectedProduct.join_way }}</p>
              <p><strong>가입 제한:</strong> {{ selectedProduct.join_deny }}</p>
              <p><strong>최고 금리:</strong> {{ selectedProduct.max_limit }}%</p>
            </template>
            
            <!-- 적금 상품인 경우 -->
            <template v-if="selectedProduct.type === 'saving'">
              <p><strong>가입 방법:</strong> {{ selectedProduct.join_way }}</p>
              <p><strong>가입 제한:</strong> {{ selectedProduct.join_member }}</p>
              <p><strong>최고 금리:</strong> {{ selectedProduct.max_limit }}%</p>
            </template>
          </div>
        </div>
        
        <div v-else class="modal-body">
          <p class="loading">상품 정보를 불러오는 중...</p>
        </div>
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

const selectedPeriod = ref(6)
const showModal = ref(false)
const selectedProduct = ref(null)
const chartCanvas = ref(null)
let chart = null

// 상품 상세 정보 보기
const showProductDetail = async (product, type) => {
  showModal.value = true
  selectedProduct.value = null

  try {
    let detailData
    if (type === 'deposit') {
      detailData = await financeStore.getDepositDetail(product.fin_prdt_cd)
    } else {
      detailData = await financeStore.getSavingDetail(product.fin_prdt_cd)
    }
    
    selectedProduct.value = {
      ...detailData,
      type
    }
  } catch (error) {
    console.error('상품 상세 정보 조회 실패:', error)
    window.alert('상품 정보를 불러오는데 실패했습니다.')
    closeModal()
  }
}

const closeModal = () => {
  showModal.value = false
  selectedProduct.value = null
}

// 상품 가입 취소
const cancelProduct = async (productId, type) => {
  if (!window.confirm('정말 이 상품의 가입을 취소하시겠습니까?')) {
    return
  }

  try {
    // 가입 취소 API 호출 구현 예정
    await accountStore.cancelProduct(productId, type)
    window.alert('상품 가입이 취소되었습니다.')
    // 프로필 정보 새로고침
    await accountStore.getProfile()
  } catch (error) {
    console.error('상품 가입 취소 실패:', error)
    window.alert('상품 가입 취소에 실패했습니다.')
  }
}

// 차트 데이터 준비
const prepareChartData = async () => {
  const depositProducts = props.profile?.joined_deposits?.map(p => ({ ...p, type: 'deposit' })) || []
  const savingProducts = props.profile?.joined_savings?.map(p => ({ ...p, type: 'saving' })) || []
  const allProducts = [...depositProducts, ...savingProducts]
  
  try {
    const ratesData = await financeStore.getProductRates(allProducts)
    
    const labels = ratesData.map(p => p.name)
    const data = ratesData.map(p => {
      // 선택된 기간에 맞는 금리 찾기
      const option = p.rates.find(r => r.save_trm === selectedPeriod.value)
      return option ? parseFloat(option.intr_rate) : 0
    })

    return {
      labels,
      datasets: [
        {
          label: `${selectedPeriod.value}개월 금리`,
          data,
          backgroundColor: 'rgba(54, 162, 235, 0.5)',
          borderColor: 'rgb(54, 162, 235)',
          borderWidth: 1
        }
      ]
    }
  } catch (error) {
    console.error('금리 데이터 준비 실패:', error)
    return {
      labels: [],
      datasets: [{
        label: `${selectedPeriod.value}개월 금리`,
        data: [],
        backgroundColor: 'rgba(54, 162, 235, 0.5)',
        borderColor: 'rgb(54, 162, 235)',
        borderWidth: 1
      }]
    }
  }
}

// 차트 업데이트
const updateChart = async () => {
  if (chart) {
    chart.destroy()
  }

  if (!chartCanvas.value) return

  const ctx = chartCanvas.value.getContext('2d')
  const chartData = await prepareChartData()
  
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

// 컴포넌트 마운트 시 차트 생성
onMounted(() => {
  updateChart()
})

// 선택된 기간이 변경될 때 차트 업데이트
watch(selectedPeriod, () => {
  updateChart()
})

// 프로필 데이터가 변경될 때 차트 업데이트
watch(() => props.profile, () => {
  updateChart()
}, { deep: true })

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
  margin: 1rem 0;
}

.period-select {
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

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  width: 90%;
  max-width: 600px;
  max-height: 80vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  padding: 0.5rem;
}

.modal-body {
  padding: 1rem 0;
}

.product-info p {
  margin-bottom: 0.8rem;
}

.loading {
  text-align: center;
  color: #666;
}
</style> 