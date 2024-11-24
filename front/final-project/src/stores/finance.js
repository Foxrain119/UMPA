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

  const detail = ref([])
  
  // 환율
  const exchanges = ref([])

  const goDetail = (product) => {
    detail.value = product
    console.log(product)
    router.push({ name: 'detail' })
  }

  const goBack = () => {
    router.go(-1)
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

  const getProducts = function () {
    // 예금 + 옵션
    axios({
      method: 'get',
      url: `${API_URL}/financial/deposit_list/`,
    })
      .then(res => {
        console.log(res.data)
        deposits.value = res.data.sort(function (a, b) {
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
      })
      .catch(err => console.log(err))
    
    // 적금 + 옵션
    axios({
      method: 'get',
      url: `${API_URL}/financial/saving_list/`,
    })
      .then(res => {
        console.log(res.data)
        savings.value = res.data.sort(function (a, b) {
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
        console.log('상품 정렬 완료')
      })
      .catch(err => console.log(err))
    
    
    
    // // 옵션
    // axios({
    //   method: 'get',
    //   url: `${API_URL}/financial/deposit_option_list/`,
    // })
    //   .then(res => {
    //     console.log(res.data)
    //     deposit_options.value = res.data
    //   })
    //   .catch(err => console.log(err))
  }


  const signUp = function (payload) {
    const { username, password1, password2 } = payload

    axios({
      method: 'post',
      url: `${API_URL}/accounts/signup/`,
      data: {
        username, password1, password2
      }
    })
      .then(res => {
        console.log('회원가입이 완료되었습니다.')
        const password = password1
        logIn({ username, password })
        router.push({ name: 'home' })
      })
      .catch(err => console.log(err))
  }

  const logIn = function (payload) {
    const username = payload.username
    const password = payload.password
    axios({
      method: 'post',
      url: `${API_URL}/accounts/login/`,
      data: {
        username, password
      }
    })
     .then(res => {
      console.log('로그인이 완료되었습니다.')
      console.log(res.data)
      token.value = res.data.key
      router.push({ name: 'home' })
     })
     .catch(err => console.log(err))
  }

  const isLogin = computed(() => {
    if (token.value === null) {
      return false
    } else {
      return true
    }
  })

  const logOut = function () {
    token.value = null
    router.push({ name: 'home' })
  }

  return { deposits, savings, detail, exchanges, goDetail, goBack, getProducts, getExchages, token, signUp, logIn, isLogin, logOut }
}, { persist: true })
