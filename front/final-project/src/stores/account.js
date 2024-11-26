import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { defineStore } from 'pinia'
import axios from 'axios'

export const useAccountStore = defineStore('account', () => {
  const API_URL = 'http://127.0.0.1:8000'
  const ARTICLES_URL = `${API_URL}/articles`
  const PROFILE_URL = `${API_URL}/profile/users`
  const articles = ref([])
  const profile = ref(null)
  const token = ref(null)
  const isEditing = ref(false)
  const router = useRouter()

  const getProfile = function () {
    if (!token.value) {
      window.alert('로그인이 필요합니다.')
      router.push({ name: 'login' })
      return
    }

    const username = localStorage.getItem('username')
    console.log('Getting profile for username:', username)

    if (!username) {
      console.error('Username not found in localStorage')
      router.push({ name: 'login' })
      return
    }

    axios({
      method: 'get',
      url: `${PROFILE_URL}/${username}/`,
      headers: {
        Authorization: `Token ${token.value}`
      }
    })
      .then(res => {
        console.log('Profile data:', res.data)
        profile.value = res.data
        isEditing.value = false
      })
      .catch(err => {
        console.error('Profile error:', err.response?.data || err)
        window.alert('프로필 정보를 불러오는 데 실패했습니다.')
        router.push({ name: 'home' })
      })
    }

  const updateProfile = function (payload) {
    const username = localStorage.getItem('username')

    axios({
      method: 'put',
      url: `${PROFILE_URL}/${username}/`,
      data: payload,
      headers: {
        'Content-Type': 'multipart/form-data',
        Authorization: `Token ${token.value}`
      }
    })
      .then(res => {
        profile.value = res.data
        isEditing.value = false
        window.alert('프로필 정보가 수정되었습니다.')
        getProfile()
      })
      .catch(err => {
        console.error('Profile update error:', err.response?.data || err)
        window.alert('프로필 정보 수정에 실패했습니다.')
      })
  }

  const signUp = function (payload) {
    const { username, password1, password2, email, phone, age, nickname } = payload

    axios({
      method: 'post',
      url: `${API_URL}/accounts/signup/`,
      data: {
        username, password1, password2, email, phone, age, nickname
      }
    })
      .then(res => {
        window.alert('회원가입이 완료되었습니다.')
        const password = password1
        logIn({ email, password })
        router.push({ name: 'home' })
      })
      .catch(err => console.log(err))
  }

  const logIn = async function (payload) {
    try {
      const { email, password } = payload
      
      const loginRes = await axios({
        method: 'post',
        url: `${API_URL}/accounts/login/`,
        data: { email, password }
      })
      
      token.value = loginRes.data.key
      
      // 사용자 정보 가져오기
      const userRes = await axios({
        method: 'get',
        url: `${API_URL}/accounts/user/`,
        headers: {
          Authorization: `Token ${loginRes.data.key}`
        }
      })
      
      localStorage.setItem('username', userRes.data.username)
      
      // 프로필 정보 즉시 가져오기
      await getProfile()
      
      router.push({ name: 'home' })
    } catch (error) {
      console.error('Login error:', error.response || error)
      window.alert('로그인에 실패했습니다.')
    }
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
    localStorage.removeItem('username')
    profile.value = null
    router.push({ name: 'home' })
    window.alert('로그아웃이 완료되었습니다.')
  }

  const deleteAccount = async function () {
    const username = localStorage.getItem('username')
    
    try {
      await axios({
        method: 'delete',
        url: `${PROFILE_URL}/${username}/`,
        headers: {
          Authorization: `Token ${token.value}`
        }
      })
      
      // 회원 탈퇴 후 로그아웃 처리
      token.value = null
      profile.value = null
      isEditing.value = false
      localStorage.removeItem('username')
      
    } catch (error) {
      console.error('Delete account error:', error.response?.data || error)
      throw error // 에러를 상위로 전파하여 컴포넌트에서 처리할 수 있도록 함
    }
  }

  // 상품 가입 취소
  const cancelProduct = async function (productId, type) {
    const username = localStorage.getItem('username')
    
    try {
      await axios({
        method: 'delete',
        url: `${PROFILE_URL}/${username}/products/cancel/`,
        data: {
          fin_prdt_cd: productId,
          product_type: type
        },
        headers: {
          Authorization: `Token ${token.value}`
        }
      })
      
      // 프로필 정보 갱신
      await getProfile()
      
    } catch (error) {
      console.error('상품 가입 취소 실패:', error.response?.data || error)
      throw error
    }
  }

  // 상품 가입
  const joinProduct = async function (productData) {
    const username = localStorage.getItem('username')
    
    try {
      await axios({
        method: 'post',
        url: `${PROFILE_URL}/${username}/products/join/`,
        data: productData,
        headers: {
          Authorization: `Token ${token.value}`
        }
      })
      
      // 프로필 정보 갱신
      await getProfile()
      
    } catch (error) {
      console.error('상품 가입 실패:', error.response?.data || error)
      throw error
    }
  }

  return { API_URL, ARTICLES_URL, PROFILE_URL, articles, profile, token, isEditing, signUp, logIn, isLogin, logOut, getProfile, updateProfile, deleteAccount, cancelProduct, joinProduct }
}, { persist: true })
