import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { defineStore } from 'pinia'
import axios from 'axios'

export const useFinanceStore = defineStore('finance', () => {
  const API_URL = 'http://127.0.0.1:8000'
  const token = ref(null)
  const router = useRouter()

  // 금융 상품
  const deposits = ref([])
  const savings = ref([])
  const detail = ref({})
  
  // 환율
  const exchanges = ref([])

  const goDetail = (product) => {
    const product_type = product.rsrv_type_nm ? 'saving' : 'deposit'
    
    detail.value = {
      ...product,
      product_type
    }
    
    // 상품 ID를 포함한 URL로 이동
    router.push({ 
      name: 'product_detail',
      params: { productId: product.fin_prdt_cd }
    })
  }

  const goBack = () => {
    // 이전 경로가 프로필 페이지인 경우
    if (router.options.history.state.back?.includes('/profile')) {
      router.push({ 
        name: 'profile',
        query: { tab: 'products' }  // 가입 상품 관리 탭으로 이동
      })
    } else {
      router.go(-1)  // 그 외의 경우 이전 페이지로 이동
    }
  }


  const getExchages = function () {
    axios({
      method: 'get',
      url: `${API_URL}/exchanges/list/`
    })
    .then(res => {
      console.log(res.data)
      exchanges.value = res.data
    })
    .catch(err => console.log(err))
  }

  // 예금 상품 목록 조회
  const getDepositList = async function () {
    try {
      const response = await axios({
        method: 'get',
        url: `${API_URL}/financial/deposit_list/`,
      })
      deposits.value = response.data
    } catch (error) {
      console.error('예금 상품 목록 조회 실패:', error)
      throw error
    }
  }

  // 적금 상품 목록 조회
  const getSavingList = async function () {
    try {
      const response = await axios({
        method: 'get',
        url: `${API_URL}/financial/saving_list/`,
      })
      savings.value = response.data
    } catch (error) {
      console.error('적금 상품 목록 조회 실패:', error)
      throw error
    }
  }

  // 전체 상품 목록 조회
  const getProducts = async function () {
    try {
      const response = await axios.get(`${API_URL}/financial/products/`)
      deposits.value = response.data.deposits
      savings.value = response.data.savings
    } catch (error) {
      console.error('상품 목록 조회 실패:', error)
      throw error
    }
  }

  // 예금 상품 상세 정보 조회
  const getDepositDetail = async (fin_prdt_cd) => {
    try {
      const response = await axios.get(`${API_URL}/financial/deposit_list/${fin_prdt_cd}/`)
      return response.data
    } catch (error) {
      console.error('예금 상품 상세 정보 조회 실패:', error)
      throw error
    }
  }

  // 적금 상품 상세 정보 조회
  const getSavingDetail = async (fin_prdt_cd) => {
    try {
      const response = await axios.get(`${API_URL}/financial/saving_list/${fin_prdt_cd}/`)
      return response.data
    } catch (error) {
      console.error('적금 상품 상세 정보 조회 실패:', error)
      throw error
    }
  }

  // 상품의 금리 정보 조회
  const getProductRates = async (products) => {
    const rates = []
    
    for (const product of products) {
      try {
        let detail
        if (product.type === 'deposit') {
          detail = await getDepositDetail(product.fin_prdt_cd)
        } else {
          detail = await getSavingDetail(product.fin_prdt_cd)
        }
        
        // 선택된 기간에 맞는 금리 정보 추출
        const rate = {
          name: `${product.kor_co_nm} ${product.fin_prdt_nm}`,
          rates: detail.options || []  // 옵션에서 금리 정보 추출
        }
        rates.push(rate)
      } catch (error) {
        console.error(`상품 ${product.fin_prdt_cd} 금리 정보 조회 실패:`, error)
      }
    }
    
    return rates
  }

  // 상품 상세 정보 조회
  const getProductDetail = async (productId) => {
    try {
      // 상품 타입에 따라 적절한 API 엔드포인트 호출
      const response = await axios.get(`${API_URL}/financial/products/${productId}/`)
      return response.data
    } catch (error) {
      console.error('상품 상세 정보 조회 실패:', error)
      throw error
    }
  }

  return { deposits, savings, detail, exchanges, goDetail, goBack, getProducts, getExchages, token, getDepositList, getSavingList, getDepositDetail, getSavingDetail, getProductRates, getProductDetail
  }
}, { persist: true })
