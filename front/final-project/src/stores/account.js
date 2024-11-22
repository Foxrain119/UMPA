import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { defineStore } from 'pinia'
import axios from 'axios'

export const useAccountStore = defineStore('account', () => {
  const API_URL = 'http://127.0.0.1:8000'
  const ARTICLES_URL = `${API_URL}/articles`
  const PROFILE_URL = `${API_URL}/profile`
  const token = ref(null)
  const router = useRouter()
  const profile = ref(null)
  const userInfo = ref([])

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

  const getUserInfo = function () {
    axios({
      method: 'get',
      url: `${PROFILE_URL}/user_info/`,
      headers: {
        Authorization: `Token ${token.value}`
      }
    })
    .then(res => {
      console.log(res.data)
      userInfo.value = res.data
    })
    .catch(err => console.log(err))
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

  const logIn = function (payload) {
    const email = payload.email
    const password = payload.password

    axios({
      method: 'post',
      url: `${API_URL}/accounts/login/`,
      data: {
        email, password
      }
    })
     .then(res => {
       console.log('Login response:', res.data)  // 로그인 응답 데이터 확인
       token.value = res.data.key

       // username이 응답에 포함되어 있는지 확인
       if (res.data.username) {
         localStorage.setItem('username', res.data.username)
         console.log('Stored username:', res.data.username)
       } else {
         // username이 없다면 추가 요청으로 사용자 정보 가져오기
         return axios({
           method: 'get',
           url: `${API_URL}/accounts/user/`,
           headers: {
             Authorization: `Token ${res.data.key}`
           }
         })
       }
     })
     .then(userRes => {
       if (userRes) {
         localStorage.setItem('username', userRes.data.username)
         console.log('Stored username from user info:', userRes.data.username)
         getProfile()
       }
       router.push({ name: 'home' })
     })
     .catch(err => {
       console.error('Login error:', err.response || err)
       window.alert('로그인에 실패했습니다.')
     })
  }

  const isLogin = computed(() => {
    if (token.value === null) {
      return false
    } else {
      return true
    }
  })

  const logOut = function () {
    window.alert('로그아웃이 완료되었습니다.')
    token.value = null
    router.push({ name: 'home' })
  }

  return { token, userInfo, getProfile, getUserInfo, signUp, logIn, isLogin, logOut }
}, { persist: true })